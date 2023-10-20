import static java.nio.charset.StandardCharsets.US_ASCII;
import static java.nio.file.Files.newBufferedReader;
import static java.nio.file.Files.newByteChannel;
import static java.nio.file.StandardOpenOption.READ;
import static java.nio.file.StandardOpenOption.WRITE;
import static java.nio.file.Paths.get;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.CharBuffer;
import java.nio.charset.Charset;
import java.nio.charset.CharsetDecoder;
import java.nio.charset.CharsetEncoder;
import java.nio.charset.CoderResult;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.regex.Pattern;
import java.util.stream.LongStream;
import java.util.stream.IntStream;
import java.util.stream.Collectors;

public class AsciiOrNULCharset extends Charset {
  AsciiOrNULCharset() {
    super("vc", new String[0]);
  }

  @Override
  public boolean contains(Charset cs) {
    return cs instanceof AsciiOrNULCharset;
  }

  @Override
  public CharsetDecoder newDecoder() {
    return new CharsetDecoder(this, 1.0f, 1.0f) {
      @Override
      protected CoderResult decodeLoop(ByteBuffer src, CharBuffer dst) {
        int position = src.position();
        try {
            for (; src.hasRemaining(); ++position) {
                if (!dst.hasRemaining()) { return CoderResult.OVERFLOW; }
                dst.put((char) Math.max(src.get(), 0));
            }
            return CoderResult.UNDERFLOW;
        } finally {
          src.position(position);
        }
      }
    };
  }

  @Override
  public CharsetEncoder newEncoder() {
    return new CharsetEncoder(this, 1.0f, 1.0f) {
      @Override
      protected CoderResult encodeLoop(CharBuffer src, ByteBuffer dst) {
        int position = src.position();
        try {
            for (; src.hasRemaining(); ++position) {
              byte c = (byte) Math.max(src.get(), 0);
              if (!dst.hasRemaining()) { return CoderResult.OVERFLOW; }
              dst.put(c);
            }
            return CoderResult.UNDERFLOW;
        } finally {
            src.position(position);
        }
      }
    };
  }
}

AsciiOrNULCharset ASCII_OR_NUL = new AsciiOrNULCharset();

// {
//   final String theTarget = "#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:";
//
//   System.out.printf("trgt: '%s', hashcode: %d%n",
//     theTarget,
//     theTarget.hashCode());
//
//   doTheDeed();
//
//   System.out.printf("trgt: '%s', hashcode: %d%n",
//     theTarget,
//     theTarget.hashCode());
// }

void doTheDeed() throws IOException {
  try (var channel=newByteChannel(get("/proc/self/mem"),READ,WRITE)) {
    newBufferedReader(Paths.get("/proc/self/maps"), US_ASCII).lines()
      .map(line -> line.split("\\s+"))
      .filter(l -> l.length == 5) // only memory locations
      .filter(l -> l[1].startsWith("rw")) // read-write permissions
      .map(l -> l[0].split(Pattern.quote("-"))) // take address
      .map(a -> Arrays.stream(a) // parse to long array
        .mapToLong(s -> Long.parseLong(s, 16)).toArray())
      .flatMapToLong(b -> LongStream.iterate(b[0], i->i<b[1], i->i+4096))
      .forEach(from -> {
        try {
          channel.position(from);
          var buf = ByteBuffer.allocate(4096);
          if (channel.read(buf) == -1) return; // stream end
          var array = buf.array();
          var page = new String(array, new AsciiOrNULCharset());
          var match = Pattern.compile("(#:){18}").matcher(page);
          if (match.find()) {
            channel.position(from + match.start());
            var dest = "colorless green ideas sleep furiously";
            channel.write(ByteBuffer.wrap(dest.getBytes()));
          }
        } catch (IOException e) { throw new RuntimeException(e); }
      });
  }
}
