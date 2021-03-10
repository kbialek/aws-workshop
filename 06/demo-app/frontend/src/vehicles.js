import * as React from "react";
import {List, Datagrid, TextField, NumberField, TextInput, NumberInput, SimpleForm, Edit, Create} from 'react-admin';

export const VehicleList = props => (
    <List {...props}>
      <Datagrid rowClick="edit">
        <TextField source="id"/>
        <TextField source="brand"/>
        <TextField source="model"/>
        <NumberField source="year"/>
      </Datagrid>
    </List>
);

export const VehicleEdit = props => (
    <Edit {...props}>
      <SimpleForm>
        <TextInput source="id"/>
        <TextInput source="brand"/>
        <TextInput source="model"/>
        <NumberInput source="year"/>
      </SimpleForm>
    </Edit>
);

export const VehicleCreate = props => (
    <Create {...props}>
      <SimpleForm>
        <TextInput source="brand"/>
        <TextInput source="model"/>
        <NumberInput source="year"/>
      </SimpleForm>
    </Create>
);
