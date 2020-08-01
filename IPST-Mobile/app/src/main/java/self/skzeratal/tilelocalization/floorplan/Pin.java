package self.skzeratal.tilelocalization.floorplan;

import android.graphics.Color;
import android.widget.ImageView;

public class Pin {
    public ImageView imageView;
    public String name;
    public int x;
    public int y;

    public Pin(ImageView imageView, String name, int x, int y) {
        this.imageView = imageView;
        this.name = name;
        this.x = x;
        this.y = y;

        imageView.setBackgroundColor(Color.GREEN);
    }

    public void show() {
        imageView.setBackgroundColor(Color.RED);
    }
}