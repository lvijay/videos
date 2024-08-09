/*
 * Simple, toy implementation of Mockito.  This is a slightly
 * modified, more elaborated version of the code shown on the YouTube
 * video: https://youtu.be/1Lt0NJcI2AQ.
 *
 * Run instructions:
 * 
 * The simplest way to run this code, thanks to JEP330, is just
 *
 * <code>java -ea ToyMockito</code>
 *
 * Alternatively, you can also compile and run it as follows:
 *
 * <pre><code>
 * javac ToyMockito.java
 * java -cp . -ea ToyMockitoTest
 * </code></pre>
 *
 * Don't forget to enable assertions with the flag <code>-ea</code>.
 */
import java.util.HashMap;
import java.util.Map;

class ToyMockitoTest {
    public static void main(String[] args) {
        /*
         * Assert uninitialized mocks return defaults.
         */
        var mylist1 = ToyMockito.mock();
        assert mylist1.get(3) == null;
        assert mylist1.get(1) == null;
        assert mylist1.get(41) == null;
        assert mylist1.size() == 0;

        /*
         * Assert positive cases.
         */
        ToyMockito.when(mylist1.size()).thenReturn(123);
        assert mylist1.size() == 123;

        /*
         * Assert different mocks have their own behavior.
         */
        var mylist2 = ToyMockito.mock();
        ToyMockito.when(mylist2.size()).thenReturn(2718);
        assert mylist2.size() == 2718;
        assert null == mylist2.get(29);

        ToyMockito.when(mylist2.get(29)).thenReturn("m229");
        assert "m229".equals(mylist2.get(29));
        assert null == mylist1.get(29);
        mylist1.get(31);

        ToyMockito.when(null).thenReturn("m131");
        assert mylist1.get(31).equals("m131");

        try {
            assert false;
            throw new RuntimeException("Enable assertions with -ea");
        } catch (AssertionError e) {
            System.out.println("All tests have passed");
        }
    }
}

interface MList {
    int size();
    String get(int i);
}

interface ThenReturn {
    void thenReturn(Object value);
}

class ToyMockito {
    static ThenReturn THENRETURN = null;
    static class MLst implements MList {
        private int sizeval;
        private Map<Integer, String> getval = new HashMap<>();
        public int size() {
            THENRETURN = v -> sizeval = (int) v;
            return sizeval;
        }
        public String get(int i) {
            THENRETURN = v -> getval.put(i, (String) v);
            return getval.get(i);
        }
    }
    public static ThenReturn when(Object o) {
        return THENRETURN;
    }
    static MList mock() {
        return new MLst();
    }
}
