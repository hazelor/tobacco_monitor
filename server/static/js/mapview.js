window.onload=function() {
    render();

}
var colors = [ "#66a50f", "#aaaaaa", "#ff3c3c","#ff8b61"];
var statuses = ["OK","Inactive", "Error","Warning"];

function render(){
    var toMercator = OpenLayers.Projection.transforms['EPSG:4326']['EPSG:3857'];
    _ = this._;
    var popupTemplate = _.template(this.$('#map-popup-template').html(), null, {variable:'model'});
    $.ajax({
        url:'/api/device',
        type:'get',
        dataType:'text',
        timeout: 1800,
        success:function(data, status){
            var map = new OpenLayers.Map("map",{projection:"EPSG:3857"});
            //var osm = new OpenLayers.Layer.OSM();

            var osm = new OpenLayers.Layer.OSM("OpenStreetMap", [
                  '//a.tile.openstreetmap.org/${z}/${x}/${y}.png',
                  '//b.tile.openstreetmap.org/${z}/${x}/${y}.png',
                  '//c.tile.openstreetmap.org/${z}/${x}/${y}.png']);

            var j_data = $.parseJSON(data);
            var features = j_data.map(function(val) {
              //var loc = val.get('location') || {};
              return new OpenLayers.Feature.Vector(
                toMercator(new OpenLayers.Geometry.Point(val.lon, val.lat)),
                  {
                     id : val['mac'],
                     status: statuses[val['status']],
                     //abbreviation : val.get('abbreviation'),
                     location_description : val['location'],
                     //ecosystem : val.get('ecosystem')
                  },
                  {
                     fillColor : colors[val['status']],
                     fillOpacity : 0.8,
                     strokeColor : '#4d4d4d',
                     strokeOpacity : 1,
                     strokeWidth : 1,
                     pointRadius : 8
                  });
            });

            // create the layer with listeners to create and destroy popups
            var vector = new OpenLayers.Layer.Vector("Points",{
              eventListeners:{

                'featureselected':function(evt){
                  var feature = evt.feature;
                  var popup = new OpenLayers.Popup.FramedCloud("popup",
                        OpenLayers.LonLat.fromString(feature.geometry.toShortString()),
                        null,
                        popupTemplate(feature.attributes),
                        null,
                        true);
                  feature.popup = popup;
                  map.addPopup(popup);

                  //if(licor.currentUser){
                  //  OpenLayers.Event.observe(view.el, 'mousedown', function(evt) {
                  //      location.href=licor.stations.url+feature.attributes.id;
                  //    }, false);
                  //}
                },

                'featureunselected':function(evt){
                  var feature = evt.feature;
                  map.removePopup(feature.popup);
                  feature.popup.destroy();
                  feature.popup = null;
                }
              }
            });

            vector.addFeatures(features);

            // create the select feature control
            var selector = new OpenLayers.Control.SelectFeature(vector,{
              hover:true,
              autoActivate:true
            });

            map.addLayers([osm, vector]);
            map.addControl(selector);
            //map.zoomToMaxExtent();

            var center = toMercator({y:27.958,x:107.7125});
            map.setCenter(new OpenLayers.LonLat(center.x, center.y), 6);
        }
    })
}
