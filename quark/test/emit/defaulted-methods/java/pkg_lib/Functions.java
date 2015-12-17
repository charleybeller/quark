package pkg_lib;

public class Functions {





/* BEGIN_BUILTIN */


    public static io.datawire.quark.runtime.JSONObject toJSON(Object obj) {
        io.datawire.quark.runtime.JSONObject result = new io.datawire.quark.runtime.JSONObject();
        if ((obj)==(null) || ((obj) != null && (obj).equals(null))) {
            (result).setNull();
            return result;
        }
        Class cls = new Class(io.datawire.quark.runtime.Builtins._getClass(obj));
        Integer idx = 0;
        if (((cls).name)==("String") || (((cls).name) != null && ((cls).name).equals("String"))) {
            (result).setString((String) (obj));
            return result;
        }
        if (((((((cls).name)==("byte") || (((cls).name) != null && ((cls).name).equals("byte"))) || (((cls).name)==("short") || (((cls).name) != null && ((cls).name).equals("short")))) || (((cls).name)==("int") || (((cls).name) != null && ((cls).name).equals("int")))) || (((cls).name)==("long") || (((cls).name) != null && ((cls).name).equals("long")))) || (((cls).name)==("float") || (((cls).name) != null && ((cls).name).equals("float")))) {
            (result).setNumber(obj);
            return result;
        }
        if (((cls).name)==("List") || (((cls).name) != null && ((cls).name).equals("List"))) {
            (result).setList();
            java.util.ArrayList<Object> list = (java.util.ArrayList<Object>) (obj);
            while ((idx) < ((list).size())) {
                (result).setListItem(idx, Functions.toJSON((list).get(idx)));
                idx = (idx) + (1);
            }
            return result;
        }
        if (((cls).name)==("Map") || (((cls).name) != null && ((cls).name).equals("Map"))) {
            (result).setObject();
            java.util.HashMap<String,Object> map = (java.util.HashMap<String,Object>) (obj);
            return result;
        }
        (result).setObjectItem(("$class"), ((new io.datawire.quark.runtime.JSONObject()).setString((cls).id)));
        java.util.ArrayList<Field> fields = (cls).getFields();
        while ((idx) < ((fields).size())) {
            (result).setObjectItem((((fields).get(idx)).name), (Functions.toJSON(((io.datawire.quark.runtime.QObject) (obj))._getField(((fields).get(idx)).name))));
            idx = (idx) + (1);
        }
        return result;
    }

/* END_BUILTIN */

/* BEGIN_BUILTIN */


    public static Object fromJSON(Class cls, io.datawire.quark.runtime.JSONObject json) {
        if (((json)==(null) || ((json) != null && (json).equals(null))) || ((json).isNull())) {
            return null;
        }
        Integer idx = 0;
        if (((cls).name)==("List") || (((cls).name) != null && ((cls).name).equals("List"))) {
            java.util.ArrayList<Object> list = (java.util.ArrayList<Object>) ((cls).construct(new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}))));
            while ((idx) < ((json).size())) {
                (list).add(Functions.fromJSON(((cls).parameters).get(0), (json).getListItem(idx)));
                idx = (idx) + (1);
            }
            return list;
        }
        java.util.ArrayList<Field> fields = (cls).getFields();
        Object result = (cls).construct(new java.util.ArrayList(java.util.Arrays.asList(new Object[]{})));
        while ((idx) < ((fields).size())) {
            Field f = (fields).get(idx);
            idx = (idx) + (1);
            if ((((f).type).name)==("String") || ((((f).type).name) != null && (((f).type).name).equals("String"))) {
                String s = ((json).getObjectItem((f).name)).getString();
                ((io.datawire.quark.runtime.QObject) (result))._setField((f).name, s);
                continue;
            }
            if ((((f).type).name)==("float") || ((((f).type).name) != null && (((f).type).name).equals("float"))) {
                Double flt = ((json).getObjectItem((f).name)).getNumber();
                ((io.datawire.quark.runtime.QObject) (result))._setField((f).name, flt);
                continue;
            }
            if ((((f).type).name)==("int") || ((((f).type).name) != null && (((f).type).name).equals("int"))) {
                if (!(((json).getObjectItem((f).name)).isNull())) {
                    Integer i = ((int) Math.round(((json).getObjectItem((f).name)).getNumber()));
                    ((io.datawire.quark.runtime.QObject) (result))._setField((f).name, i);
                }
                continue;
            }
            if ((((f).type).name)==("bool") || ((((f).type).name) != null && (((f).type).name).equals("bool"))) {
                if (!(((json).getObjectItem((f).name)).isNull())) {
                    Boolean b = ((json).getObjectItem((f).name)).getBool();
                    ((io.datawire.quark.runtime.QObject) (result))._setField((f).name, b);
                }
                continue;
            }
            ((io.datawire.quark.runtime.QObject) (result))._setField((f).name, Functions.fromJSON((f).type, (json).getObjectItem((f).name)));
        }
        return result;
    }

/* END_BUILTIN */


    public static void main() {
        pkg.T1 t1 = new pkg.T1();
        (t1).foo();
        (t1).bar();
        do{System.out.println("===");System.out.flush();}while(false);
        pkg.T2 t2 = new pkg.T2();
        (t2).foo();
        (t2).bar();
        do{System.out.println("===");System.out.flush();}while(false);
        pkg.T3 t3 = new pkg.T3();
        (t3).foo();
        (t3).bar();
        do{System.out.println("===");System.out.flush();}while(false);
        pkg.T4 t4 = new pkg.T4();
        (t4).foo();
        (t4).bar();
        do{System.out.println("===");System.out.flush();}while(false);
        pkg.T5 t5 = new pkg.T5();
        (t5).foo();
        (t5).bar();
    }


    public static Object _construct(String className, java.util.ArrayList<Object> args) {
        if ((className)==("Class") || ((className) != null && (className).equals("Class"))) {
            return new Class((String) ((args).get(0)));
        }
        if ((className)==("Field") || ((className) != null && (className).equals("Field"))) {
            return new Field((Class) ((args).get(0)), (String) ((args).get(1)));
        }
        if ((className)==("List<Object>") || ((className) != null && (className).equals("List<Object>"))) {
            return new java.util.ArrayList<Object>();
        }
        if ((className)==("List<Field>") || ((className) != null && (className).equals("List<Field>"))) {
            return new java.util.ArrayList<Field>();
        }
        if ((className)==("List<Class>") || ((className) != null && (className).equals("List<Class>"))) {
            return new java.util.ArrayList<Class>();
        }
        if ((className)==("List<String>") || ((className) != null && (className).equals("List<String>"))) {
            return new java.util.ArrayList<String>();
        }
        if ((className)==("Map<Object,Object>") || ((className) != null && (className).equals("Map<Object,Object>"))) {
            return new java.util.HashMap<Object,Object>();
        }
        if ((className)==("Map<String,Object>") || ((className) != null && (className).equals("Map<String,Object>"))) {
            return new java.util.HashMap<String,Object>();
        }
        if ((className)==("ResponseHolder") || ((className) != null && (className).equals("ResponseHolder"))) {
            return new ResponseHolder();
        }
        if ((className)==("Client") || ((className) != null && (className).equals("Client"))) {
            return new Client((io.datawire.quark.runtime.Runtime) ((args).get(0)), (String) ((args).get(1)));
        }
        if ((className)==("Server<Object>") || ((className) != null && (className).equals("Server<Object>"))) {
            return new Server<Object>((io.datawire.quark.runtime.Runtime) ((args).get(0)), (args).get(1));
        }
        if ((className)==("pkg.T1") || ((className) != null && (className).equals("pkg.T1"))) {
            return new pkg.T1();
        }
        if ((className)==("pkg.T2") || ((className) != null && (className).equals("pkg.T2"))) {
            return new pkg.T2();
        }
        if ((className)==("pkg.T3") || ((className) != null && (className).equals("pkg.T3"))) {
            return new pkg.T3();
        }
        if ((className)==("pkg.T4") || ((className) != null && (className).equals("pkg.T4"))) {
            return new pkg.T4();
        }
        if ((className)==("pkg.T5") || ((className) != null && (className).equals("pkg.T5"))) {
            return new pkg.T5();
        }
        return null;
    }


    public static java.util.ArrayList<Field> _fields(String className) {
        if ((className)==("Class") || ((className) != null && (className).equals("Class"))) {
            return new java.util.ArrayList(java.util.Arrays.asList(new Object[]{new Field(new Class("String"), "id"), new Field(new Class("String"), "name"), new Field(new Class("List<Class>"), "parameters")}));
        }
        if ((className)==("Field") || ((className) != null && (className).equals("Field"))) {
            return new java.util.ArrayList(java.util.Arrays.asList(new Object[]{new Field(new Class("Class"), "type"), new Field(new Class("String"), "name")}));
        }
        if ((className)==("List<Object>") || ((className) != null && (className).equals("List<Object>"))) {
            return new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
        }
        if ((className)==("List<Field>") || ((className) != null && (className).equals("List<Field>"))) {
            return new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
        }
        if ((className)==("List<Class>") || ((className) != null && (className).equals("List<Class>"))) {
            return new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
        }
        if ((className)==("List<String>") || ((className) != null && (className).equals("List<String>"))) {
            return new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
        }
        if ((className)==("Map<Object,Object>") || ((className) != null && (className).equals("Map<Object,Object>"))) {
            return new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
        }
        if ((className)==("Map<String,Object>") || ((className) != null && (className).equals("Map<String,Object>"))) {
            return new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
        }
        if ((className)==("ResponseHolder") || ((className) != null && (className).equals("ResponseHolder"))) {
            return new java.util.ArrayList(java.util.Arrays.asList(new Object[]{new Field(new Class("HTTPResponse"), "response"), new Field(new Class("String"), "failure")}));
        }
        if ((className)==("Client") || ((className) != null && (className).equals("Client"))) {
            return new java.util.ArrayList(java.util.Arrays.asList(new Object[]{new Field(new Class("Runtime"), "runtime"), new Field(new Class("String"), "url")}));
        }
        if ((className)==("Server<Object>") || ((className) != null && (className).equals("Server<Object>"))) {
            return new java.util.ArrayList(java.util.Arrays.asList(new Object[]{new Field(new Class("Runtime"), "runtime"), new Field(new Class("Object"), "impl")}));
        }
        if ((className)==("pkg.T1") || ((className) != null && (className).equals("pkg.T1"))) {
            return new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
        }
        if ((className)==("pkg.T2") || ((className) != null && (className).equals("pkg.T2"))) {
            return new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
        }
        if ((className)==("pkg.T3") || ((className) != null && (className).equals("pkg.T3"))) {
            return new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
        }
        if ((className)==("pkg.T4") || ((className) != null && (className).equals("pkg.T4"))) {
            return new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
        }
        if ((className)==("pkg.T5") || ((className) != null && (className).equals("pkg.T5"))) {
            return new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
        }
        return (java.util.ArrayList<Field>) (null);
    }


    public static void _class(Class cls) {
        if (((cls).id)==("Class") || (((cls).id) != null && ((cls).id).equals("Class"))) {
            (cls).name = "Class";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
            return;
        }
        if (((cls).id)==("Field") || (((cls).id) != null && ((cls).id).equals("Field"))) {
            (cls).name = "Field";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
            return;
        }
        if (((cls).id)==("List<Object>") || (((cls).id) != null && ((cls).id).equals("List<Object>"))) {
            (cls).name = "List";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{new Class("Object")}));
            return;
        }
        if (((cls).id)==("List<Field>") || (((cls).id) != null && ((cls).id).equals("List<Field>"))) {
            (cls).name = "List";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{new Class("Field")}));
            return;
        }
        if (((cls).id)==("List<Class>") || (((cls).id) != null && ((cls).id).equals("List<Class>"))) {
            (cls).name = "List";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{new Class("Class")}));
            return;
        }
        if (((cls).id)==("List<String>") || (((cls).id) != null && ((cls).id).equals("List<String>"))) {
            (cls).name = "List";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{new Class("String")}));
            return;
        }
        if (((cls).id)==("Map<Object,Object>") || (((cls).id) != null && ((cls).id).equals("Map<Object,Object>"))) {
            (cls).name = "Map";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{new Class("Object"), new Class("Object")}));
            return;
        }
        if (((cls).id)==("Map<String,Object>") || (((cls).id) != null && ((cls).id).equals("Map<String,Object>"))) {
            (cls).name = "Map";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{new Class("String"), new Class("Object")}));
            return;
        }
        if (((cls).id)==("ResponseHolder") || (((cls).id) != null && ((cls).id).equals("ResponseHolder"))) {
            (cls).name = "ResponseHolder";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
            return;
        }
        if (((cls).id)==("Service") || (((cls).id) != null && ((cls).id).equals("Service"))) {
            (cls).name = "Service";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
            return;
        }
        if (((cls).id)==("Client") || (((cls).id) != null && ((cls).id).equals("Client"))) {
            (cls).name = "Client";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
            return;
        }
        if (((cls).id)==("Server<Object>") || (((cls).id) != null && ((cls).id).equals("Server<Object>"))) {
            (cls).name = "Server";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{new Class("Object")}));
            return;
        }
        if (((cls).id)==("pkg.A") || (((cls).id) != null && ((cls).id).equals("pkg.A"))) {
            (cls).name = "pkg.A";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
            return;
        }
        if (((cls).id)==("pkg.B") || (((cls).id) != null && ((cls).id).equals("pkg.B"))) {
            (cls).name = "pkg.B";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
            return;
        }
        if (((cls).id)==("pkg.C") || (((cls).id) != null && ((cls).id).equals("pkg.C"))) {
            (cls).name = "pkg.C";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
            return;
        }
        if (((cls).id)==("pkg.T1") || (((cls).id) != null && ((cls).id).equals("pkg.T1"))) {
            (cls).name = "pkg.T1";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
            return;
        }
        if (((cls).id)==("pkg.T2") || (((cls).id) != null && ((cls).id).equals("pkg.T2"))) {
            (cls).name = "pkg.T2";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
            return;
        }
        if (((cls).id)==("pkg.T3") || (((cls).id) != null && ((cls).id).equals("pkg.T3"))) {
            (cls).name = "pkg.T3";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
            return;
        }
        if (((cls).id)==("pkg.T4") || (((cls).id) != null && ((cls).id).equals("pkg.T4"))) {
            (cls).name = "pkg.T4";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
            return;
        }
        if (((cls).id)==("pkg.T5") || (((cls).id) != null && ((cls).id).equals("pkg.T5"))) {
            (cls).name = "pkg.T5";
            (cls).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
            return;
        }
        (cls).name = (cls).id;
    }


    public static Object _invoke(String className, Object object, String method, java.util.ArrayList<Object> args) {
        if ((className)==("Class") || ((className) != null && (className).equals("Class"))) {
            if ((method)==("getId") || ((method) != null && (method).equals("getId"))) {
                Class tmp_0 = (Class) (object);
                return (tmp_0).getId();
            }
            if ((method)==("getName") || ((method) != null && (method).equals("getName"))) {
                Class tmp_1 = (Class) (object);
                return (tmp_1).getName();
            }
            if ((method)==("getParameters") || ((method) != null && (method).equals("getParameters"))) {
                Class tmp_2 = (Class) (object);
                return (tmp_2).getParameters();
            }
            if ((method)==("construct") || ((method) != null && (method).equals("construct"))) {
                Class tmp_3 = (Class) (object);
                return (tmp_3).construct((java.util.ArrayList<Object>) ((args).get(0)));
            }
            if ((method)==("getFields") || ((method) != null && (method).equals("getFields"))) {
                Class tmp_4 = (Class) (object);
                return (tmp_4).getFields();
            }
            if ((method)==("getField") || ((method) != null && (method).equals("getField"))) {
                Class tmp_5 = (Class) (object);
                return (tmp_5).getField((String) ((args).get(0)));
            }
            if ((method)==("invoke") || ((method) != null && (method).equals("invoke"))) {
                Class tmp_6 = (Class) (object);
                return (tmp_6).invoke((args).get(0), (String) ((args).get(1)), (java.util.ArrayList<Object>) ((args).get(2)));
            }
        }
        if ((className)==("Field") || ((className) != null && (className).equals("Field"))) {}
        if ((className)==("List<Object>") || ((className) != null && (className).equals("List<Object>"))) {}
        if ((className)==("List<Field>") || ((className) != null && (className).equals("List<Field>"))) {}
        if ((className)==("List<Class>") || ((className) != null && (className).equals("List<Class>"))) {}
        if ((className)==("List<String>") || ((className) != null && (className).equals("List<String>"))) {}
        if ((className)==("Map<Object,Object>") || ((className) != null && (className).equals("Map<Object,Object>"))) {}
        if ((className)==("Map<String,Object>") || ((className) != null && (className).equals("Map<String,Object>"))) {}
        if ((className)==("ResponseHolder") || ((className) != null && (className).equals("ResponseHolder"))) {
            if ((method)==("onHTTPResponse") || ((method) != null && (method).equals("onHTTPResponse"))) {
                ResponseHolder tmp_7 = (ResponseHolder) (object);
                (tmp_7).onHTTPResponse((io.datawire.quark.runtime.HTTPRequest) ((args).get(0)), (io.datawire.quark.runtime.HTTPResponse) ((args).get(1)));
                return null;
            }
            if ((method)==("onHTTPError") || ((method) != null && (method).equals("onHTTPError"))) {
                ResponseHolder tmp_8 = (ResponseHolder) (object);
                (tmp_8).onHTTPError((io.datawire.quark.runtime.HTTPRequest) ((args).get(0)), (String) ((args).get(1)));
                return null;
            }
        }
        if ((className)==("Service") || ((className) != null && (className).equals("Service"))) {
            if ((method)==("getURL") || ((method) != null && (method).equals("getURL"))) {
                Service tmp_9 = (Service) (object);
                return (tmp_9).getURL();
            }
            if ((method)==("getRuntime") || ((method) != null && (method).equals("getRuntime"))) {
                Service tmp_10 = (Service) (object);
                return (tmp_10).getRuntime();
            }
            if ((method)==("rpc") || ((method) != null && (method).equals("rpc"))) {
                Service tmp_11 = (Service) (object);
                return (tmp_11).rpc((String) ((args).get(0)), (args).get(1));
            }
        }
        if ((className)==("Client") || ((className) != null && (className).equals("Client"))) {
            if ((method)==("getRuntime") || ((method) != null && (method).equals("getRuntime"))) {
                Client tmp_12 = (Client) (object);
                return (tmp_12).getRuntime();
            }
            if ((method)==("getURL") || ((method) != null && (method).equals("getURL"))) {
                Client tmp_13 = (Client) (object);
                return (tmp_13).getURL();
            }
        }
        if ((className)==("Server<Object>") || ((className) != null && (className).equals("Server<Object>"))) {
            if ((method)==("getRuntime") || ((method) != null && (method).equals("getRuntime"))) {
                Server<Object> tmp_14 = (Server<Object>) (object);
                return (tmp_14).getRuntime();
            }
            if ((method)==("onHTTPRequest") || ((method) != null && (method).equals("onHTTPRequest"))) {
                Server<Object> tmp_15 = (Server<Object>) (object);
                (tmp_15).onHTTPRequest((io.datawire.quark.runtime.HTTPRequest) ((args).get(0)), (io.datawire.quark.runtime.HTTPResponse) ((args).get(1)));
                return null;
            }
            if ((method)==("onServletError") || ((method) != null && (method).equals("onServletError"))) {
                Server<Object> tmp_16 = (Server<Object>) (object);
                (tmp_16).onServletError((String) ((args).get(0)), (String) ((args).get(1)));
                return null;
            }
        }
        if ((className)==("pkg.A") || ((className) != null && (className).equals("pkg.A"))) {
            if ((method)==("foo") || ((method) != null && (method).equals("foo"))) {
                pkg.A tmp_17 = (pkg.A) (object);
                (tmp_17).foo();
                return null;
            }
            if ((method)==("bar") || ((method) != null && (method).equals("bar"))) {
                pkg.A tmp_18 = (pkg.A) (object);
                (tmp_18).bar();
                return null;
            }
        }
        if ((className)==("pkg.B") || ((className) != null && (className).equals("pkg.B"))) {
            if ((method)==("bar") || ((method) != null && (method).equals("bar"))) {
                pkg.B tmp_19 = (pkg.B) (object);
                (tmp_19).bar();
                return null;
            }
        }
        if ((className)==("pkg.C") || ((className) != null && (className).equals("pkg.C"))) {
            if ((method)==("foo") || ((method) != null && (method).equals("foo"))) {
                pkg.C tmp_20 = (pkg.C) (object);
                (tmp_20).foo();
                return null;
            }
        }
        if ((className)==("pkg.T1") || ((className) != null && (className).equals("pkg.T1"))) {
            if ((method)==("foo") || ((method) != null && (method).equals("foo"))) {
                pkg.T1 tmp_21 = (pkg.T1) (object);
                (tmp_21).foo();
                return null;
            }
        }
        if ((className)==("pkg.T2") || ((className) != null && (className).equals("pkg.T2"))) {
            if ((method)==("foo") || ((method) != null && (method).equals("foo"))) {
                pkg.T2 tmp_22 = (pkg.T2) (object);
                (tmp_22).foo();
                return null;
            }
        }
        if ((className)==("pkg.T3") || ((className) != null && (className).equals("pkg.T3"))) {
            if ((method)==("foo") || ((method) != null && (method).equals("foo"))) {
                pkg.T3 tmp_23 = (pkg.T3) (object);
                (tmp_23).foo();
                return null;
            }
        }
        if ((className)==("pkg.T4") || ((className) != null && (className).equals("pkg.T4"))) {}
        if ((className)==("pkg.T5") || ((className) != null && (className).equals("pkg.T5"))) {
            if ((method)==("foo") || ((method) != null && (method).equals("foo"))) {
                pkg.T5 tmp_24 = (pkg.T5) (object);
                (tmp_24).foo();
                return null;
            }
        }
        return null;
    }
}