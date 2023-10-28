// -*- mode: java; -*-

import static java.nio.charset.StandardCharsets.US_ASCII;
import static java.nio.file.Files.newBufferedReader;
import static java.nio.file.Files.newByteChannel;
import static java.nio.file.Paths.get;
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
import java.util.stream.IntStream;
import java.util.stream.Collectors;

public class AsciiOrNULCharset extends Charset {
  public AsciiOrNULCharset() { super("ASCIIorNUL", new String[0]); }

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

void modifyMemory() throws IOException {
  try (var channel=newByteChannel(Paths.get("/proc/self/mem"),READ,WRITE)) {
    // File format: https://man7.org/linux/man-pages/man5/proc.5.html
    // address           perms offset  dev   inode       pathname
    // 00400000-00452000 r-xp 00000000 08:02 173521      /usr/bin/dbus-daemon
    // ...
    // 00e03000-00e24000 rw-p 00000000 00:00 0           [heap]
    // 35b1800000-35b1820000 r-xp 00000000 08:02 135522  /usr/lib64/ld-2.15.so
    // 35b1a1f000-35b1a20000 r--p 0001f000 08:02 135522  /usr/lib64/ld-2.15.so
    // 35b1a20000-35b1a21000 rw-p 00020000 08:02 135522  /usr/lib64/ld-2.15.so
    // ...
    // 35b1a21000-35b1a22000 rw-p 00000000 00:00 0
    // f2c6ff8c000-7f2c7078c000 rw-p 00000000 00:00 0    [stack:986]
    // 7fffb2c0d000-7fffb2c2e000 rw-p 00000000 00:00 0   [stack]
    // 7fffb2d48000-7fffb2d49000 r-xp 00000000 00:00 0   [vdso]
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

/*
 * {
 *   final String theTarget = "#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:#:";
 *
 *   System.out.printf("trgt: '%s', hashcode: %d%n",
 *     theTarget,
 *     theTarget.hashCode());
 *
 *   modifyMemory();
 *
 *   System.out.printf("trgt: '%s', hashcode: %d%n",
 *     theTarget,
 *     theTarget.hashCode());
 * }
 */
