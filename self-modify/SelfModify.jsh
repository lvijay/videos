import static java.nio.charset.StandardCharsets.US_ASCII;
import static java.nio.file.Files.newBufferedReader;
import static java.nio.file.Files.newByteChannel;
import static java.nio.file.StandardOpenOption.READ;
import static java.nio.file.StandardOpenOption.WRITE;

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

public class AsciiOrNUL extends Charset {
  public static final AsciiOrNUL INSTANCE = new AsciiOrNUL();

  AsciiOrNUL() {
    super("vc", new String[0]);
  }

  @Override
  public boolean contains(Charset cs) {
    return cs instanceof AsciiOrNUL;
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

AsciiOrNUL ASCII_OR_NUL = new AsciiOrNUL();

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
  try (var channel=newByteChannel(Paths.get("/proc/self/mem"),READ,WRITE)) {
    newBufferedReader(Paths.get("/proc/self/maps"), US_ASCII).lines()
      .map(line -> line.split("\\s+"))
      // address         perms offset   dev   inode pathname
      // 00e24000-011f7000   rw-p  00000000 00:00 0   [heap]
      // ...
      // 35b1a21000-35b1a22000 rw-p  00000000 00:00 0
      // 35b1c00000-35b1dac000 r-xp  00000000 08:02 135870 /usr/bin/g++
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
          if (channel.read(buf) == -1) { return; } // end of stream
          var block = new String(buf.array(), ASCII_OR_NUL);
          var match = Pattern.compile("(?:#:){18}").matcher(block);
          if (!match.find()) { return; }
          channel.position(from + match.start());
          byte[] v = new byte[match.end() - match.start()];
          for (int i=0; i<v.length; ++i) { v[i] = (byte) ('0' + i); }
          channel.write(ByteBuffer.wrap(v));
        } catch (IOException e) { throw new RuntimeException(e); }
      });
  }
}
