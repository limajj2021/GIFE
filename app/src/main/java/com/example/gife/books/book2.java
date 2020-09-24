package com.example.gife.books;

import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;

import com.example.gife.R;
import com.github.barteksc.pdfviewer.PDFView;

public class book2 extends AppCompatActivity {
    private PDFView pdfview;
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.book_two);

        pdfview = findViewById(R.id.pdfViewer);

        pdfview.useBestQuality(true);
        pdfview.enableSwipe(true);
        pdfview.fitToWidth();
        pdfview.fromAsset("inferno_danbrown.pdf").load();

    }
}

