package com.example.hackathon;

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

import com.google.android.material.snackbar.Snackbar;

public class RegistrationActivity extends AppCompatActivity {

    Button backButton, reg_button;
    TextView textViewReg;
    EditText editTextEmail, editTextPassword, editTextRepeatPassword, editTextName;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_registration);

        reg_button = findViewById(R.id.reg_button);
        backButton = findViewById(R.id.backButton);
        textViewReg = findViewById(R.id.textViewReg);
        backButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intentLog = new Intent(RegistrationActivity.this, LoginActivity.class);
                intentLog.addFlags(Intent.FLAG_ACTIVITY_NO_ANIMATION);
                startActivityForResult(intentLog, 0);
                overridePendingTransition(0,0);
                finish();
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
            }
        });
    }
    private void snack() {
        editTextEmail = findViewById(R.id.editTextEmail);
        editTextPassword = findViewById(R.id.editTextPassword);
        editTextRepeatPassword = findViewById(R.id.editTextRepeatPassword);
        editTextName = findViewById(R.id.editTextName);

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
}