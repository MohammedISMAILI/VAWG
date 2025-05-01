import React from 'react';
import MapComponent from '@terrestris/react-geo/dist/Map/MapComponent/MapComponent.tsx';
import OlMap from 'ol/Map';
import OlView from 'ol/View';
import OlLayerTile from 'ol/layer/Tile';
import OlSourceOsm from 'ol/source/OSM';

import './App.css';
import 'ol/ol.css';
import 'antd/dist/antd.min.css';
import './react-geo.css';


const layer = new OlLayerTile({
  source: new OlSourceOsm()
});

const center = [ 788453.4890155146, 6573085.729161344 ];

const map = new OlMap({
  view: new OlView({
    center: center,
    zoom: 16,
  }),
  layers: [layer]
});

function Map() {
  return (
    <div className="App">
      <MapComponent
        map={map}
      />
    </div>
  );
}

export default Map;