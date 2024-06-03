package com.example.hackathon;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

public class ExamAdapter extends ArrayAdapter<JSONObject> {
    int listLayout;
    ArrayList<JSONObject> examsList;
    Context context;

    public ExamAdapter(Context context, int listLayout , int field, ArrayList<JSONObject> examsList) {
        super(context, listLayout, field, examsList);
        this.context = context;
        this.listLayout=listLayout;
        this.examsList = examsList;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        View listViewItem = inflater.inflate(listLayout, null, false);
        TextView exam = listViewItem.findViewById(R.id.exam);
        try{
            exam.setText(examsList.get(position).getString("exam"));
        }catch (JSONException je){
            je.printStackTrace();
        }
        return listViewItem;
    }
}
