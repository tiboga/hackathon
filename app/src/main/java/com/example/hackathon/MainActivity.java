package com.example.hackathon;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {
    private static final String JSON_URL = "/api/task/new";
    private LinearLayout easyLevel;
    private LinearLayout mediumLevel;
    private LinearLayout hardLevel;
    Button analytics, profile;
    TextView privacy_policy;
    ListView exam;
    String selectedLevel = "easy";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);

        exam = findViewById(R.id.exam);
        profile = findViewById(R.id.profile);
        analytics = findViewById(R.id.analitics);
        easyLevel = findViewById(R.id.easyLevel);
        mediumLevel = findViewById(R.id.mediumLevel);
        hardLevel = findViewById(R.id.hardLevel);
        privacy_policy = findViewById(R.id.privacy_policy);

        loadJSONFromURL(JSON_URL, selectedLevel);

        profile.setOnClickListener(v -> {
            Intent intent = new Intent(MainActivity.this, ProfileActivity.class);
            intent.addFlags(Intent.FLAG_ACTIVITY_NO_ANIMATION);
            startActivityForResult(intent, 0);
            overridePendingTransition(0, 0);
        });
        analytics.setOnClickListener(v -> {
            Intent intent2 = new Intent(MainActivity.this, AnaliticsActivity.class);
            intent2.addFlags(Intent.FLAG_ACTIVITY_NO_ANIMATION);
            startActivityForResult(intent2, 0);
            overridePendingTransition(0, 0);
        });
        privacy_policy.setOnClickListener(v -> {
            Intent intent3 = new Intent(MainActivity.this, PrivacyPolicy.class);
            intent3.addFlags(Intent.FLAG_ACTIVITY_NO_ANIMATION);
            startActivityForResult(intent3, 0);
            overridePendingTransition(0, 0);
        });

        easyLevel.setOnClickListener(v -> {
            resetCircles();
            selectedLevel = "easy";
            easyLevel.getChildAt(0).setBackground(ContextCompat.getDrawable(MainActivity.this, R.drawable.circle_selected_green));
            loadJSONFromURL(JSON_URL, selectedLevel);
        });

        mediumLevel.setOnClickListener(v -> {
            resetCircles();
            selectedLevel = "medium";
            mediumLevel.getChildAt(0).setBackground(ContextCompat.getDrawable(MainActivity.this, R.drawable.circle_selected_yellow));
            loadJSONFromURL(JSON_URL, selectedLevel);
        });

        hardLevel.setOnClickListener(v -> {
            resetCircles();
            selectedLevel = "hard";
            hardLevel.getChildAt(0).setBackground(ContextCompat.getDrawable(MainActivity.this, R.drawable.circle_selected_red));
            loadJSONFromURL(JSON_URL, selectedLevel);
        });
    }

    private void resetCircles() {
        easyLevel.getChildAt(0).setBackground(ContextCompat.getDrawable(MainActivity.this, R.drawable.circle_selector_green));
        mediumLevel.getChildAt(0).setBackground(ContextCompat.getDrawable(MainActivity.this, R.drawable.circle_selector_yellow));
        hardLevel.getChildAt(0).setBackground(ContextCompat.getDrawable(MainActivity.this, R.drawable.circle_selector_red));
    }

    private void loadJSONFromURL(String url, String level) {
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url + "?level=" + level + "&example_type=type1&user_id=12345",
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        try {
                            JSONObject object = new JSONObject(EncodingToUTF8(response));
                            JSONArray jsonArray = object.getJSONArray("exams");
                            ArrayList<JSONObject> listItems = getArrayListFromJSONArray(jsonArray);
                            ListAdapter adapter = new ExamAdapter(getApplicationContext(), R.layout.activity_main, R.id.exam, listItems);
                            exam.setAdapter(adapter);
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(getApplicationContext(), error.getMessage(), Toast.LENGTH_SHORT).show();
                    }
                });
        RequestQueue requestQueue = Volley.newRequestQueue(this);
        requestQueue.add(stringRequest);
    }

    private ArrayList<JSONObject> getArrayListFromJSONArray(JSONArray jsonArray) {
        ArrayList<JSONObject> aList = new ArrayList<>();
        try {
            if (jsonArray != null) {
                for (int i = 0; i < jsonArray.length(); i++) {
                    aList.add(jsonArray.getJSONObject(i));
                }
            }
        } catch (JSONException js) {
            js.printStackTrace();
        }
        return aList;
    }

    public static String EncodingToUTF8(String response) {
        try {
            byte[] code = response.toString().getBytes("ISO-8859-1");
            response = new String(code, "UTF-8");
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
            return null;
        }
        return response;
    }
}
