package com.example.gife;

import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;

import com.github.barteksc.pdfviewer.PDFView;

public class Aviophobia extends AppCompatActivity {
    private PDFView pdfview;
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.aviophobia);

        pdfview = findViewById(R.id.pdfViewer);

        pdfview.useBestQuality(true);
        pdfview.enableSwipe(true);
        pdfview.fitToWidth();
        pdfview.fromAsset("aviophobia.pdf").load();

    }
}
