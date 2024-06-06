package com.example.hackathon;

import com.android.volley.toolbox.JsonObjectRequest;

import com.example.hackathon.UrlInfo;
import com.example.hackathon.CurrentUser;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.AppCompatButton;

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

public class RegistrationActivity extends AppCompatActivity {

    Button backButton, reg_button;
    private static final String REGISTER_URL = UrlInfo.ret_url() + "/api/user/auth";
    TextView textViewReg;
    EditText editTextEmail, editTextPassword, editTextRepeatPassword, editTextName;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_registration);

        reg_button = findViewById(R.id.reg_button);
        backButton = findViewById(R.id.backButton);
        textViewReg = findViewById(R.id.textViewReg);
        editTextEmail = findViewById(R.id.editTextEmail);
        editTextPassword = findViewById(R.id.editTextPassword);
        editTextRepeatPassword = findViewById(R.id.editTextRepeatPassword);
        editTextName = findViewById(R.id.editTextName);

        backButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                onBackPressed();
            }
        });

        textViewReg.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                textViewReg.setText(R.string.login_underline);
                Intent intentLog = new Intent(RegistrationActivity.this, LoginActivity.class);
                intentLog.addFlags(Intent.FLAG_ACTIVITY_NO_ANIMATION);
                startActivityForResult(intentLog, 0);
                overridePendingTransition(0,0);
                finish();
            }
        });
        reg_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                snack();
                registerUser();
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
        if (TextUtils.isEmpty(editTextRepeatPassword.getText().toString())) {
            snackbarMake("Упс! Вы не повторили пароль!");
            return;

        }
        if (TextUtils.isEmpty(editTextName.getText().toString())) {
            snackbarMake("Упс! Вы не ввели имя пользователя!");
            return;

        }
    }
    private void snackbarMake(String textSnack) {
        Snackbar.make(findViewById(R.id.snackLayout), textSnack, Snackbar.LENGTH_SHORT)
                .setBackgroundTint(getResources().getColor(R.color.green))
                .setTextColor(Color.WHITE)
                .show();
    }
    private void registerUser() {
        String login = editTextEmail.getText().toString();
        String username = editTextName.getText().toString();
        String password = editTextPassword.getText().toString();
        String repeatPassword = editTextRepeatPassword.getText().toString();

        if (!password.equals(repeatPassword)) {
            Toast.makeText(this, "Passwords do not match", Toast.LENGTH_LONG).show();
            return;
        }
        Map<String, String> postParam = new HashMap<String, String>();
        postParam.put("login", login);
        postParam.put("username", username);
        postParam.put("password", password);
        JsonObjectRequest stringRequest = new JsonObjectRequest
                (Request.Method.POST, REGISTER_URL,new JSONObject(postParam),

                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            String status = response.getString("Status");

                            if (status.equals("ok")) {
                                int user_id = response.getInt("user_id");
                                FileOutputStream fos = null;


                                try {
                                    fos = openFileOutput("current_user.txt", MODE_APPEND);
                                    String uid = ";" + Integer.toString(user_id);
                                    fos.write(uid.getBytes());
                                } catch (IOException ex) {
                                } finally {
                                    try {
                                        if (fos != null)
                                            fos.close();
                                    } catch (IOException ex) {
                                    }
                                }
                                Toast.makeText(RegistrationActivity.this, "Registration successful!", Toast.LENGTH_LONG).show();

                                Intent intent = new Intent(RegistrationActivity.this, LoginActivity.class);
                                startActivity(intent);
                                finish();


                            } else {
                                String description = response.getString("description");
                                Toast.makeText(RegistrationActivity.this, "Ошибка: " + description, Toast.LENGTH_LONG).show();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(RegistrationActivity.this, "Error: " + error.getMessage(), Toast.LENGTH_LONG).show();
                    }
                }) {
            @Override
            protected Map<String, String> getParams() {
                Map<String, String> params = new HashMap<>();
                params.put("login", login);
                params.put("username", username);
                params.put("password", password);
                return params;
            }
        };

        RequestQueue requestQueue = Volley.newRequestQueue(this);
        requestQueue.add(stringRequest);
    }
}