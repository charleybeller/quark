package quark_ffi_signatures_md;

public class interfaces_T1_foo_Method extends quark.reflect.Method implements io.datawire.quark.runtime.QObject {
    public interfaces_T1_foo_Method() {
        super("quark.void", "foo", new java.util.ArrayList(java.util.Arrays.asList(new Object[]{})));
    }
    public Object invoke(Object object, java.util.ArrayList<Object> args) {
        interfaces.T1 obj = (interfaces.T1) (object);
        (obj).foo();
        return null;
    }
    public String _getClass() {
        return (String) (null);
    }
    public Object _getField(String name) {
        return null;
    }
    public void _setField(String name, Object value) {}
}
