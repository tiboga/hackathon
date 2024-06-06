package com.example.hackathon;

import com.example.hackathon.CurrentUser;
import com.example.hackathon.UrlInfo;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {
    private static final String JSON_URL = UrlInfo.ret_url() + "/api/task/new";
    private LinearLayout easyLevel;
    private LinearLayout mediumLevel;
    private LinearLayout hardLevel;
    Button analytics, profile, next_button, check_button;
    TextView privacy_policy;
    TextView exam;
    String selectedLevel = "easy";
    String selectedType = "addition";
    RelativeLayout layoutTypeEquality, layoutTypeNumericalEx;

    // Тип знака между частями примера
    String[] itemType = {"Равенство", "Неравенство", "Числовой пример"};
    AutoCompleteTextView autoCompleteText;
    ArrayAdapter<String> adapterTypes;

    // Тип примера если выбрано равенство
    String[] itemTypeEquality = {"Квадратное", "Неквадратное",};
    AutoCompleteTextView autoCompleteTextEquality;
    ArrayAdapter<String> adapterTypesEquality;

    // Тип примера если выбран числовой пример
    String[] itemTypeNumericalEx = {"Сложение", "Вычитание", "Деление", "Умножение"};
    AutoCompleteTextView autoCompleteTextNumericalEx;
    ArrayAdapter<String> adapterTypesNumericalEx;


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
        next_button = findViewById(R.id.next_button);
        check_button = findViewById(R.id.check_button);

        layoutTypeEquality = findViewById(R.id.layoutTypeEquality);
        layoutTypeNumericalEx = findViewById(R.id.layoutTypeNumericalEx);

        layoutTypeEquality.setVisibility(View.GONE);
        layoutTypeNumericalEx.setVisibility(View.GONE);

        autoCompleteText = findViewById(R.id.autoCompleteText);
        adapterTypes = new ArrayAdapter<String>(this, R.layout.list_item_types, itemType);
        autoCompleteText.setAdapter(adapterTypes);

        autoCompleteTextEquality = findViewById(R.id.autoCompleteTextEquality);
        adapterTypesEquality = new ArrayAdapter<String>(this, R.layout.list_item_types, itemTypeEquality);
        autoCompleteTextEquality.setAdapter(adapterTypesEquality);

        autoCompleteTextNumericalEx = findViewById(R.id.autoCompleteTextNumericalEx);
        adapterTypesNumericalEx = new ArrayAdapter<String>(this, R.layout.list_item_types, itemTypeNumericalEx);
        autoCompleteTextNumericalEx.setAdapter(adapterTypesNumericalEx);
//        FileOutputStream fos = null;
//        try {
//            fos = openFileOutput("current_user.txt", MODE_APPEND);
//            fos.write("sssssssss".getBytes());
//            Toast.makeText(this, "Файл сохранен", Toast.LENGTH_SHORT).show();
//        }
//        catch(IOException ex) {
//
//            Toast.makeText(this, ex.getMessage(), Toast.LENGTH_SHORT).show();
//        }
//        finally{
//            try{
//                if(fos!=null)
//                    fos.close();
//            }
//            catch(IOException ex){
//
//                Toast.makeText(this, ex.getMessage(), Toast.LENGTH_SHORT).show();
//            }
//        }
//        {
//            try {
//                JSONObject obj = new JSONObject((Map) new FileReader("CurrentUser.json"));
//                try {
//                    String str = obj.getString("id");
//                    privacy_policy.setText(str);
//                } catch (JSONException e) {
//                    throw new RuntimeException(e);
//                }
//            } catch (FileNotFoundException e) {
//                throw new RuntimeException(e);
//            }
//        }


        // Тип знака между частями примера
        autoCompleteText.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int position, long id) {

                String item = adapterView.getItemAtPosition(position).toString();

                // Обработка нажатий
                switch (item) {
                    case "Равенство":
                        layoutTypeEquality.setVisibility(View.VISIBLE);
                        layoutTypeNumericalEx.setVisibility(View.GONE);
                        selectedType = "equality";
                        loadJSONFromURL(JSON_URL);
                        break;
                    case "Неравенство":
                        layoutTypeEquality.setVisibility(View.GONE);
                        layoutTypeNumericalEx.setVisibility(View.GONE);
                        selectedType = "x_inequality";
                        loadJSONFromURL(JSON_URL);
                        break;
                    case "Числовой пример":
                        layoutTypeEquality.setVisibility(View.GONE);
                        layoutTypeNumericalEx.setVisibility(View.VISIBLE);
                        selectedType = "addition";
                        loadJSONFromURL(JSON_URL);
                        break;
                    default:
                        break;
                }
            }
        });

        // Тип примера если выбрано равенство
        autoCompleteTextEquality.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int position, long id) {

                String item2 = adapterView.getItemAtPosition(position).toString();
                privacy_policy.setText(item2);
                // Обработка нажатий
                switch (item2) {
                    case "Квадратное":
                        selectedType = "quadratic";
                        loadJSONFromURL(JSON_URL);
                        break;
                    case "Неквадратное":
                        selectedType = "equality";
                        loadJSONFromURL(JSON_URL);
                        break;
                    default:
                        break;
                }
            }
        });

        // Тип примера если выбран числовой пример
        autoCompleteTextNumericalEx.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int position, long id) {

                String item3 = adapterView.getItemAtPosition(position).toString();
                privacy_policy.setText(item3);
                // Обработка нажатий
                switch (item3) {
                    case "Сложение":
                        selectedType = "addition";
                        loadJSONFromURL(JSON_URL);
                        break;
                    case "Вычитание":
                        selectedType = "subtraction";
                        loadJSONFromURL(JSON_URL);
                        break;
                    case "Деление":
                        selectedType = "division";
                        loadJSONFromURL(JSON_URL);
                        break;
                    case "Умножение":
                        selectedType = "multiplication";
                        loadJSONFromURL(JSON_URL);
                        break;
                    default:
                        break;
                }
            }
        });

        loadJSONFromURL(JSON_URL);

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
            loadJSONFromURL(JSON_URL);
        });

        mediumLevel.setOnClickListener(v -> {
            resetCircles();
            selectedLevel = "medium";
            mediumLevel.getChildAt(0).setBackground(ContextCompat.getDrawable(MainActivity.this, R.drawable.circle_selected_yellow));
            loadJSONFromURL(JSON_URL);
        });

        hardLevel.setOnClickListener(v -> {
            resetCircles();
            selectedLevel = "hard";
            hardLevel.getChildAt(0).setBackground(ContextCompat.getDrawable(MainActivity.this, R.drawable.circle_selected_red));
            loadJSONFromURL(JSON_URL);
        });
        next_button.setOnClickListener(v->
        {
            loadJSONFromURL(JSON_URL);
        });
        check_button.setOnClickListener(v->
        {
            FileInputStream fin = null;
            try {
                fin = openFileInput("current_task.txt");
                byte[] bytes = new byte[fin.available()];
                fin.read(bytes);
                String text = new String(bytes);
                String[] sp = text.split(";");
                if (sp.length >= 1) {
                    text = sp[sp.length - 1];
                }

                privacy_policy.setText(text);
            } catch (IOException ex) {

                Toast.makeText(this, ex.getMessage(), Toast.LENGTH_SHORT).show();
            } finally {

                try {
                    if (fin != null)
                        fin.close();
                } catch (IOException ex) {

                    Toast.makeText(this, ex.getMessage(), Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    private void resetCircles() {
        easyLevel.getChildAt(0).setBackground(ContextCompat.getDrawable(MainActivity.this, R.drawable.circle_selector_green));
        mediumLevel.getChildAt(0).setBackground(ContextCompat.getDrawable(MainActivity.this, R.drawable.circle_selector_yellow));
        hardLevel.getChildAt(0).setBackground(ContextCompat.getDrawable(MainActivity.this, R.drawable.circle_selector_red));
    }

    private void loadJSONFromURL(String url) {
        FileInputStream fin = null;
        int int_id;
        int_id = 0;
        try {
            fin = openFileInput("current_user.txt");
            byte[] bytes = new byte[fin.available()];
            fin.read(bytes);
            String text = new String(bytes);
            String[] sp = text.split(";");
            if (sp.length >= 1) {
                text = sp[sp.length - 1];
                int_id = Integer.parseInt(text);
            }
        } catch (IOException ex) {

            Toast.makeText(this, ex.getMessage(), Toast.LENGTH_SHORT).show();
        } finally {

            try {
                if (fin != null)
                    fin.close();
            } catch (IOException ex) {

                Toast.makeText(this, ex.getMessage(), Toast.LENGTH_SHORT).show();
            }
        }
        Map<String, String> postParam = new HashMap<String, String>();
        postParam.put("level", selectedLevel);
        postParam.put("example_type", selectedType);
        if (int_id == 0) {
            postParam.put("user_id", "MOB");
        } else {
            postParam.put("user_id", Integer.toString(int_id));
        }
        JsonObjectRequest stringRequest = new JsonObjectRequest
                (Request.Method.POST, url, new JSONObject(postParam),
                        new Response.Listener<JSONObject>() {
                            @Override
                            public void onResponse(JSONObject response) {
                                try {
                                    String string_1 = response.getString("Status");
                                    String string_2 = response.getString("task");
                                    String string_3 = response.getString("true_answer");
                                    String string_4 = response.getString("task_id");
                                            FileOutputStream fos = null;
                                    try {
                                        fos = openFileOutput("current_task.txt", MODE_APPEND);
                                        String out_string;
                                        out_string = ":" + string_2 + "," + string_3 + "," + string_4;
                                        fos.write(out_string.getBytes());
                                    }
                                    catch(IOException ex) {
                                    }
                                    finally{
                                        try{
                                            if(fos!=null)
                                                fos.close();
                                        }
                                        catch(IOException ex){
                                        }
                                    }
                                    exam.setText(string_2);
                                } catch (JSONException e) {
                                    throw new RuntimeException(e);
                                }

                            }
                        },
                        new Response.ErrorListener() {
                            @Override
                            public void onErrorResponse(VolleyError error) {
                                exam.setText("ERROR");
                            }
                        }
                );

//        } {
//
//                    @Override
//                    public void onResponse(String response) {
//                        try {
//                            JSONObject object = new JSONObject(EncodingToUTF8(response));
//                            JSONObject pipipu = object.getJSONObject("pipipu");
//                            String value = pipipu.getString("value");
////                            JSONArray jsonArray = object.getJSONArray("value");
////                            ArrayList<JSONObject> listItems = getArrayListFromJSONArray(jsonArray);
////                            ListAdapter adapter = new ExamAdapter(getApplicationContext(), R.layout.activity_main, R.id.exam, listItems);
////                            exam.setAdapter(adapter);
//                            privacy_policy.setText(value);
//
//                        } catch (JSONException e) {
//                            e.printStackTrace();
//                        }
//                    }
//                },
//                new Response.ErrorListener() {
//                    @Override
//                    public void onErrorResponse(VolleyError error) {
//                        Toast.makeText(getApplicationContext(), error.getMessage(), Toast.LENGTH_SHORT).show();
//                    }


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
