package autocast;

public class Functions {

    static autocast_md.Root root = new autocast_md.Root();


    public static void foo(String s) {
        do{System.out.println(s);System.out.flush();}while(false);
    }


    public static void main() {
        Object o = "Hello World!";
        String s = (String) (o);
        String s2;
        s2 = (String) (o);
        Functions.foo((String) (o));
    }
}