package quark_ffi_signatures_md;

public class inheritance_t2_A extends quark.reflect.Class implements io.datawire.quark.runtime.QObject {
    public static quark.reflect.Class singleton = new inheritance_t2_A();
    public inheritance_t2_A() {
        super("inheritance.t2.A");
        (this).name = "inheritance.t2.A";
        (this).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
        (this).fields = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
        (this).methods = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
        (this).parents = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{"quark.Object"}));
    }
    public Object construct(java.util.ArrayList<Object> args) {
        return new inheritance.t2.A();
    }
    public Boolean isAbstract() {
        return false;
    }
    public String _getClass() {
        return (String) (null);
    }
    public Object _getField(String name) {
        return null;
    }
    public void _setField(String name, Object value) {}
}
