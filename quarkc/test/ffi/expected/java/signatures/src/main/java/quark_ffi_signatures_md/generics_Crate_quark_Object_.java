package quark_ffi_signatures_md;

public class generics_Crate_quark_Object_ extends quark.reflect.Class implements io.datawire.quark.runtime.QObject {
    public static quark.reflect.Class singleton = new generics_Crate_quark_Object_();
    public generics_Crate_quark_Object_() {
        super("generics.Crate<quark.Object>");
        (this).name = "generics.Crate";
        (this).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{"quark.Object"}));
        (this).fields = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{new quark.reflect.Field("generics.Box<quark.Object>", "box"), new quark.reflect.Field("generics.Box<quark.int>", "ibox")}));
        (this).methods = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{new generics_Crate_quark_Object__set_Method(), new generics_Crate_quark_Object__get_Method()}));
        (this).parents = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{"quark.Object"}));
    }
    public Object construct(java.util.ArrayList<Object> args) {
        return new generics.Crate<Object>();
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
