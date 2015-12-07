/*
 * Copyright 2015 datawire. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// Quark Runtime
/* jshint node: true */

(function () {
    "use strict";

    exports.util = require("util");

    function quark_toString(value) {
        if (value === null) {
            return "null";
        }
        if (Array.isArray(value)) {
            return "[" + value.map(quark_toString).join(", ") + "]";
        }
        return value.toString();
    }
    exports.toString = quark_toString;

    function print(message) {
        console.log(quark_toString(message));
    }
    exports.print = print;

    function modulo(a, b) {
        return (a % b + b) % b;
    }
    exports.modulo = modulo;

    function map_get(m, key) {
        if (m.has(key)) {
            return m.get(key);
        }
        return null;
    }
    exports.map_get = map_get;

    var execSync = require("child_process").execSync;

    function url_get(url) {
        var resBuffer = execSync('curl -s -w "\n\n%{http_code}" ' + url);
        var res = resBuffer.toString("UTF-8");
        if (res.substr(-5) === "\n\n200") {
            return res.substr(0, res.length - 5);
        }
        return "error";
    }
    exports.url_get = url_get;

    var querystring = require("querystring");
    function urlencode(map) {
        var obj = {};
        map.forEach(function (value, key) {
            obj[key.toString()] = value
        })
        return querystring.stringify(obj);
    }
    exports.urlencode = urlencode;

    function sleep(seconds) {
        execSync("sleep " + seconds);
    }
    exports.sleep = sleep;

    function JSONObject() {
        this.value = null;
    }
    exports.JSONObject = JSONObject;

    function JSONObject_getType() {
        var t = typeof this.value;
        if (t === "object") {
            if (this.value === null)
                return "null";
            if (Array.isArray(this.value))
                return "list";
        }
        return t;
    }
    JSONObject.prototype.getType = JSONObject_getType;

    function JSONObject_wrap(value) {
        var j = new JSONObject();
        j.value = value;
        return j;
    }

    function JSONObject_getObjectItem(key) {
        var value = this.value[key];
        if (value === undefined) {
            return this.undefined();
        }
        return JSONObject_wrap(value);
    }
    JSONObject.prototype.getObjectItem = JSONObject_getObjectItem;

    function JSONObject_getListItem(index) {
        var value = this.value[index];
        if (value === undefined) {
            return this.undefined();
        }
        return JSONObject_wrap(value);
    }
    JSONObject.prototype.getListItem = JSONObject_getListItem;

    function JSONObject_getString() {
        if (typeof this.value !== 'string') {
            return null;
        }
        return this.value;
    }
    JSONObject.prototype.getString = JSONObject_getString;

    function JSONObject_isString() {
        return typeof this.value == 'string';
    }
    JSONObject.prototype.isString = JSONObject_isString;

    function JSONObject_getNumber() {
        if (typeof this.value !== 'number') {
            return null;
        }
        return this.value;
    }
    JSONObject.prototype.getNumber = JSONObject_getNumber;

    function JSONObject_isNumber() {
        return typeof this.value == 'number';
    }
    JSONObject.prototype.isNumber = JSONObject_isNumber;

    function JSONObject_getBool() {
        if (typeof this.value !== 'boolean') {
            return null;
        }
        return this.value;
    }
    JSONObject.prototype.getBool = JSONObject_getBool;

    function JSONObject_isBool() {
        return typeof this.value == 'boolean';
    }
    JSONObject.prototype.isBool = JSONObject_isBool;

    function JSONObject_isNull() {
        return this.value === null;
    }
    JSONObject.prototype.isNull = JSONObject_isNull;

    function JSONObject_isUndefined() {
        return this === _JSONObject_undefined;
    }
    JSONObject.prototype.isUndefined = JSONObject_isUndefined;

    function JSONObject_isDefined() {
        return !this.isUndefined();
    }
    JSONObject.prototype.isDefined = JSONObject_isDefined;

    var _JSONObject_undefined = new JSONObject();
    _JSONObject_undefined.value = undefined;

    function JSONObject_undefined() {
        return _JSONObject_undefined;
    }
    JSONObject.prototype.undefined = JSONObject_undefined;

    function JSONObject_toString() {
        return JSON.stringify(this.value);
    }
    JSONObject.prototype.toString = JSONObject_toString;


    function JSONObject_setString(value) {
        this.value = value;
        return this;
    }
    JSONObject.prototype.setString = JSONObject_setString;
    _JSONObject_undefined.setString = undefined;

    function JSONObject_setNumber(value) {
        this.value = value;
        return this;
    }
    JSONObject.prototype.setNumber = JSONObject_setNumber;
    _JSONObject_undefined.setNumber = undefined;

    function JSONObject_setBool(value) {
        this.value = !!value;
        return this;
    }
    JSONObject.prototype.setBool = JSONObject_setBool;
    _JSONObject_undefined.setBool = undefined;

    function JSONObject_setNull() {
        this.value = null;
        return this;
    }
    JSONObject.prototype.setNull = JSONObject_setNull;
    _JSONObject_undefined.setNull = undefined;

    function JSONObject_setObject() {
        this.value = {};
        return this;
    }
    JSONObject.prototype.setObject = JSONObject_setObject;
    _JSONObject_undefined.setObject = undefined;

    function JSONObject_isObject() {
        return this.getType() == 'object';
    }
    JSONObject.prototype.isObject = JSONObject_isObject;

    function JSONObject_setList() {
        this.value = [];
        return this;
    }
    JSONObject.prototype.setList = JSONObject_setList;
    _JSONObject_undefined.setList = undefined;

    function JSONObject_isList() {
        return this.getType() == 'list';
    }
    JSONObject.prototype.isList = JSONObject_isList;

    function JSONObject_setObjectItem(key, value) {
        if (this.getType() !== 'object') {
            this.value = {};
        }
        this.value[key] = value.value;
        return this;
    }
    JSONObject.prototype.setObjectItem = JSONObject_setObjectItem;
    _JSONObject_undefined.setObjectItem = undefined;

    function JSONObject_setListItem(index, value) {
        if (this.getType() !== 'list') {
            this.value = [];
        }
        for(var i = this.value.length; i < index - 1; i++) {
            this.value[i] = null;
        }
        this.value[index] = value.value;
        return this;
    }
    JSONObject.prototype.setListItem = JSONObject_setListItem;
    _JSONObject_undefined.setListItem = undefined;

    function JSONObject_size() {
        if (this.getType() == 'list') {
            return this.value.length;
        } else if (this.getType() == 'object') {
            return Object.keys(this.value).length;
        } else {
            return 1;
        }
    }
    JSONObject.prototype.size = JSONObject_size;
    _JSONObject_undefined.size = undefined;

    function json_from_string(json) {
        var raw = JSON.parse(json);
        var value = new JSONObject();
        value.value = raw;
        return value;
    }

    exports.json_from_string = json_from_string;

    function HTTPRequest(url) {
        this.url = url;
        this.method = "GET";
        this.body = null;
        this.headers = {};
    }

    function HTTPRequest_setMethod(method) {
        this.method = method;
    }
    HTTPRequest.prototype.setMethod = HTTPRequest_setMethod;

    function HTTPRequest_setBody(body) {
        this.body = body;
    }
    HTTPRequest.prototype.setBody = HTTPRequest_setBody;

    function HTTPRequest_setHeader(key, value) {
        this.headers[key] = value;
    }
    HTTPRequest.prototype.setHeader = HTTPRequest_setHeader;

    exports.HTTPRequest = HTTPRequest;

    function _Buffer(arg) {
        if (Buffer.isBuffer(arg)) {
            this.data = arg;
        } else {
            this.data = new Buffer(arg)
        }
        this.be = true;
    }

    exports.Buffer = _Buffer;

    function _Buffer_capacity() {
        return this.data.length;
    }
    _Buffer.prototype.capacity = _Buffer_capacity;

    function _Buffer_getByte(index) {
        return this.data[index];
    }
    _Buffer.prototype.getByte = _Buffer_getByte;

    function _Buffer_putByte(index, value) {
        this.data[index] = value;
    }
    _Buffer.prototype.putByte = _Buffer_putByte;

    function _Buffer_getShort(index) {
        if (this.be) {
            return this.data.readInt16BE(index);
        } else {
            return this.data.readInt16LE(index);
        }
    }
    _Buffer.prototype.getShort = _Buffer_getShort;

    function _Buffer_putShort(index, value) {
        if (this.be) {
            this.data.writeInt16BE(value, index);
        } else {
            this.data.writeInt16LE(value, index);
        }
    }
    _Buffer.prototype.putShort = _Buffer_putShort;


    function _Buffer_getInt(index) {
        if (this.be) {
            return this.data.readInt32BE(index);
        } else {
            return this.data.readInt32LE(index);
        }
    }
    _Buffer.prototype.getInt = _Buffer_getInt;

    function _Buffer_putInt(index, value) {
        if (this.be) {
            this.data.writeInt32BE(value, index);
        } else {
            this.data.writeInt32LE(value, index);
        }
    }
    _Buffer.prototype.putInt = _Buffer_putInt;

    function _Buffer_getLong(index) {
        var sgn;
        if (this.be) {
            sgn = this.data.readIntBE(index, 2);
            if (-1 <= sgn && sgn <= 0) {
                return this.data.readIntBE(index + 2, 6);
            }
        } else {
            sgn = this.data.readIntLE(index + 6, 2);
            if (-1 <= sgn && sgn <= 0) {
                return this.data.readIntLE(index, 6);
            }
        }
        throw new TypeError("value out of representable range " + this.data.toString('hex', index, index+8))
    }
    _Buffer.prototype.getLong = _Buffer_getLong;

    function _Buffer_putLong(index, value) {
        var sgn = value < 0 ? -1 : 0;
        if (this.be) {
            this.data.writeIntBE(value, index+2, 6);
            this.data.writeIntBE(sgn, index, 2);
        } else {
            this.data.writeIntLE(value, index, 6);
            this.data.writeIntLE(sgn, index+6, 2);
        }
    }
    _Buffer.prototype.putLong = _Buffer_putLong;

    function _Buffer_getFloat(index) {
        if (this.be) {
            return this.data.readDoubleBE(index);
        } else {
            return this.data.readDoubleLE(index);
        }
    }
    _Buffer.prototype.getFloat = _Buffer_getFloat;

    function _Buffer_putFloat(index, value) {
        if (this.be) {
            this.data.writeDoubleBE(value, index);
        } else {
            this.data.writeDoubleLE(value, index);
        }
    }
    _Buffer.prototype.putFloat = _Buffer_putFloat;

    function _Buffer_getStringUTF8(index, length) {
        return this.data.toString(undefined, index, index + length);
    }
    _Buffer.prototype.getStringUTF8 = _Buffer_getStringUTF8;

    function _Buffer_putStringUTF8(index, value) {
        var length = Buffer.byteLength(value);
        var actual = this.data.write(value, index, length);
        if (length != actual) {
            throw new RangeError("String does not fit");
        }
        return actual;
    }
    _Buffer.prototype.putStringUTF8 = _Buffer_putStringUTF8;

    function _Buffer_getSlice(index, length) {
        var other = new _Buffer(this.data.slice(index, index + length));
        other.be = this.be;
        return other;
    }
    _Buffer.prototype.getSlice = _Buffer_getSlice;

    function _Buffer_setSlice(index, buffer, offset, length) {
        buffer.data.copy(this.data, index, offset, offset + length);
    }
    _Buffer.prototype.setSlice = _Buffer_setSlice;

    function _Buffer_littleEndian() {
        var other = new _Buffer(this.data);
        other.be = false;
        return other;
    }
    _Buffer.prototype.littleEndian = _Buffer_littleEndian;

    function _Buffer_isNetworkByteOrder() {
        return this.be;
    }
    _Buffer.prototype.isNetworkByteOrder = _Buffer_isNetworkByteOrder;

    function Codec() {
        // empty
    }

    var codec = new Codec();

    function Codec_buffer(capacity) {
        return new _Buffer(capacity);
    }
    Codec.prototype.buffer = Codec_buffer;

    function Codec_toHexdump(buffer, offset, length, spaceScale) {
        var hex = buffer.data.toString('hex', offset, offset + length);
        var stride = Math.pow(2, (spaceScale+1));
        var ret = hex.slice(0, stride);
        for (var i = stride; i < hex.length; i += stride) {
            ret = ret + " " + hex.slice(i, i + stride);
        }
        return ret;
    }
    Codec.prototype.toHexdump = Codec_toHexdump;

    function Codec_fromHexdump(hex) {
        hex = hex.replace(/[ \r\n\t]/g, "");
        hex = hex.replace(/^0[Xx]/, "");
        return new _Buffer(new Buffer(hex, "hex"));
    }
    Codec.prototype.fromHexdump = Codec_fromHexdump;

    function Codec_toBase64(buffer, offset, length) {
        return buffer.data.toString('base64', offset, offset + length);
    }
    Codec.prototype.toBase64 = Codec_toBase64;

    function Codec_fromBase64(base64) {
        return new _Buffer(new Buffer(base64, "base64"));
    }
    Codec.prototype.fromBase64 = Codec_fromBase64;

    function defaultCodec() {
        return codec;
    }

    exports.defaultCodec = defaultCodec;

    function _getClass(obj) {
        if (typeof obj == "boolean") { return "bool"; }
        if (typeof obj == "number") { return "float"; }
        if (typeof obj == "string") { return "String"; }
        if (obj instanceof Array) { return "List<Object>"; }
        if (obj instanceof Map) { return "Map<Object,Object>"; }

        if (obj._getClass) { return obj._getClass(); }

        return null;
    }
    exports._getClass = _getClass;

})();