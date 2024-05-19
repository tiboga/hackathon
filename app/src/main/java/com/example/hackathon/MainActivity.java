package com.example.hackathon;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class MainActivity extends AppCompatActivity {
    private LinearLayout easyLevel;
    private LinearLayout mediumLevel;
    private LinearLayout hardLevel;
    Button analitics, profile;
    TextView privacy_policy;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);

        profile = findViewById(R.id.profile);
        analitics = findViewById(R.id.analitics);
        easyLevel = findViewById(R.id.easyLevel);
        mediumLevel = findViewById(R.id.mediumLevel);
        hardLevel = findViewById(R.id.hardLevel);
        privacy_policy = findViewById(R.id.privacy_policy);

        profile.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, ProfileActivity.class);
                intent.addFlags(Intent.FLAG_ACTIVITY_NO_ANIMATION);
                startActivityForResult(intent, 0);
                overridePendingTransition(0,0);
            }
        });
        analitics.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent2 = new Intent(MainActivity.this, AnaliticsActivity.class);
                intent2.addFlags(Intent.FLAG_ACTIVITY_NO_ANIMATION);
                startActivityForResult(intent2, 0);
                overridePendingTransition(0,0);
            }
        });
        privacy_policy.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent3 = new Intent(MainActivity.this, PrivacyPolicy.class);
                intent3.addFlags(Intent.FLAG_ACTIVITY_NO_ANIMATION);
                startActivityForResult(intent3, 0);
                overridePendingTransition(0,0);
            }
        });
        easyLevel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                resetCircles();
                easyLevel.getChildAt(0).setBackground(ContextCompat.getDrawable(MainActivity.this, R.drawable.circle_selected_green));
            }
        });

        mediumLevel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                resetCircles();
                mediumLevel.getChildAt(0).setBackground(ContextCompat.getDrawable(MainActivity.this, R.drawable.circle_selected_yellow));
            }
        });

        hardLevel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                resetCircles();
                hardLevel.getChildAt(0).setBackground(ContextCompat.getDrawable(MainActivity.this, R.drawable.circle_selected_red));
            }
        });
    }
    private void resetCircles() {
        easyLevel.getChildAt(0).setBackground(ContextCompat.getDrawable(MainActivity.this, R.drawable.circle_selector_green));
        mediumLevel.getChildAt(0).setBackground(ContextCompat.getDrawable(MainActivity.this, R.drawable.circle_selector_yellow));
        hardLevel.getChildAt(0).setBackground(ContextCompat.getDrawable(MainActivity.this, R.drawable.circle_selector_red));
    }
}