import * as React from "react";
import {Admin, Resource} from 'react-admin';
import simpleRestProvider from 'ra-data-simple-rest';
import {VehicleCreate, VehicleEdit, VehicleList} from "./vehicles";

const dataProvider = simpleRestProvider('https://api.demo-app.pl/api');
const App = () => (
    <Admin dataProvider={dataProvider}>
      <Resource name="vehicles" list={VehicleList} edit={VehicleEdit} create={VehicleCreate} />
    </Admin>
);

export default App;
