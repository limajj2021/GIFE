package com.example.gife.books;

import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;

import com.example.gife.R;
import com.github.barteksc.pdfviewer.PDFView;

public class book4 extends AppCompatActivity {
    private PDFView pdfview;
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.book_four);

        pdfview = findViewById(R.id.pdfViewer);

        pdfview.useBestQuality(true);
        pdfview.enableSwipe(true);
        pdfview.fitToWidth();
        pdfview.fromAsset("thelittleprince.pdf").load();

    }
}
