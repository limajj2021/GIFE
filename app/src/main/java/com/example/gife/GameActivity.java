package com.example.gife;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

import com.example.gife.games.Game1;
import com.example.gife.games.Game2;
import com.example.gife.games.Game3;
import com.example.gife.games.Game4;

public class GameActivity extends AppCompatActivity {
    Button buttontictac;
    Button buttonrace;
    Button buttonsudoku;
    Button buttonmemory;
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.game_activity);
        buttontictac = (Button) findViewById(R.id.buttonctacto);
        buttonrace = (Button) findViewById(R.id.buttonrace);
        buttonsudoku = (Button) findViewById(R.id.buttonsudoku);
        buttonmemory = (Button) findViewById(R.id.buttonmemory);

        buttontictac.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(GameActivity.this, Game1.class);
                startActivity(intentLoadNewActivity);
            }

        });

        buttonrace.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(GameActivity.this, Game2.class);
                startActivity(intentLoadNewActivity);
            }

        });

        buttonsudoku.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(GameActivity.this, Game3.class);
                startActivity(intentLoadNewActivity);
            }

        });

        buttonmemory.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentLoadNewActivity = new Intent(GameActivity.this, Game4.class);
                startActivity(intentLoadNewActivity);
            }

        });

    }
}
