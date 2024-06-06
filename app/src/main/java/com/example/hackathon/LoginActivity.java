package com.example.hackathon;

import com.example.hackathon.CurrentUser;

import com.android.volley.toolbox.JsonObjectRequest;
import com.example.hackathon.UrlInfo;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.AppCompatButton;

import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.material.snackbar.Snackbar;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map;

public class LoginActivity extends AppCompatActivity {

    Button login_button, skip_btn;
    private static final String LOGIN_URL = UrlInfo.ret_url() + "/api/user/login";
    EditText editTextEmail, editTextPassword;
    TextView textViewCreate;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        skip_btn = findViewById(R.id.skip_btn);
        login_button = findViewById(R.id.login_button);
        textViewCreate = findViewById(R.id.textViewCreate);
        editTextEmail = findViewById(R.id.editTextEmail);
        editTextPassword = findViewById(R.id.editTextPassword);
        login_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                loginUser();
//                snack();
            }

        });
        textViewCreate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                textViewCreate.setText(R.string.create_underline);
                Intent intentLog = new Intent(LoginActivity.this, RegistrationActivity.class);
                intentLog.addFlags(Intent.FLAG_ACTIVITY_NO_ANIMATION);
                startActivityForResult(intentLog, 0);
                overridePendingTransition(0,0);
                finish();
            }
        });
        skip_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(LoginActivity.this, MainActivity.class);
                intent.addFlags(Intent.FLAG_ACTIVITY_NO_ANIMATION);
                startActivityForResult(intent, 0);
                overridePendingTransition(0,0);
                finish();
            }
        });
    }
    private void snack() {

        if (TextUtils.isEmpty(editTextEmail.getText().toString())) {
            snackbarMake("Упс! Вы не ввели почту!");
            return;

        }
        if (TextUtils.isEmpty(editTextPassword.getText().toString())) {
            snackbarMake("Упс! Вы не ввели пароль!");
            return;

        }
        if (TextUtils.isEmpty(editTextEmail.getText().toString()) && TextUtils.isEmpty(editTextPassword.getText().toString())) {
            snackbarMake("Заполните все поля!");

        }
    }
    private void snackbarMake(String textSnack) {
        Snackbar.make(findViewById(R.id.snackLayout), textSnack, Snackbar.LENGTH_SHORT)
                .setBackgroundTint(getResources().getColor(R.color.green))
                .setTextColor(Color.WHITE)
                .show();
    }
    private void loginUser() {
        String login = editTextEmail.getText().toString();
        String password = editTextPassword.getText().toString();
        Map<String, String> postParam = new HashMap<String, String>();
        postParam.put("login", login);
        postParam.put("password", password);
        JsonObjectRequest stringRequest = new JsonObjectRequest
                (Request.Method.POST,
                        LOGIN_URL,
                        new JSONObject(postParam),
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            String status = response.getString("Status");
                            boolean loginSuccess = response.getBoolean("login");

                            if (status.equals("ok") && loginSuccess) {
                                int id = response.getInt("id");
                                CurrentUser currentUser = new CurrentUser();
                                currentUser.login(id);
                                FileOutputStream fos = null;
                                try {
                                    fos = openFileOutput("current_user.txt", MODE_APPEND);
                                    String uid = ";" + Integer.toString(id);
                                    fos.write(uid.getBytes());
                                } catch (IOException ex) {
                                } finally {
                                    try {
                                        if (fos != null)
                                            fos.close();
                                    } catch (IOException ex) {
                                    }
                                }
//                                Toast.makeText(LoginActivity.this, "Успешный вход! ID: " + userId, Toast.LENGTH_LONG).show();
                                Intent intent = new Intent(LoginActivity.this, MainActivity.class);
                                startActivity(intent);
                                finish();
                            } else {
                                Toast.makeText(LoginActivity.this, "Ошибка! Неправильный логин или пароль", Toast.LENGTH_LONG).show();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(LoginActivity.this, "Ошибка: " + error.getMessage(), Toast.LENGTH_LONG).show();
                    }
                }) {
            @Override
            protected Map<String, String> getParams() {
                Map<String, String> params = new HashMap<>();
                params.put("login", login);
                params.put("password", password);
                return params;
            }
        };

        RequestQueue requestQueue = Volley.newRequestQueue(this);
        requestQueue.add(stringRequest);
    }
}