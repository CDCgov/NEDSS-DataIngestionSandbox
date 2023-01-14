package com.ndduc.springcomsumerdemo.helper;

import com.google.gson.JsonParser;

public class MessageHelper {
    public static String extractValue(String json, String key) {
        return JsonParser.parseString(json).getAsJsonObject().get(key).getAsString();
    }

    public static String extractId(String json) {
        return JsonParser.parseString(json).getAsJsonObject().get("_id").getAsString();
    }

    public static String extractOriginalClass(String json) {
        return JsonParser.parseString(json).getAsJsonObject().get("_class").getAsString();
    }
}
