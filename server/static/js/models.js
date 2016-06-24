(function (root) {
"use strict";

var Backbone = root.Backbone,
    _ = root._,
    licor = root.licor || (root.licor = {});

var Station = Backbone.Model.extend({
      defaults:{
        status: 0,
        permissions: {update: true, 'delete': true}
      },
      coordinates: function(){
        if(this.has('location')){
          var loc = this.get('location');
          if(loc.latitude && loc.longitude){
            return (+loc.latitude).toFixed(3)+'&deg, '+
                   (+loc.longitude).toFixed(3)+'&deg;';
          }
        }
        return '';
      },
      elevation: function(){
        if(this.has('location')){
          var loc = this.get('location');
          if(loc.elevation){
            return loc.elevation + ' m';
          }
        }
        return '';
      }
    }),
    Stations = Backbone.Collection.extend({
        model: Station,
        parse: function(response){
          return response.stations;
        }
    }),
    User = Backbone.Model.extend({
      hasRole: function(name){
        return _.contains(this.get('roles'), name);
      },
      roleLabels: function(){
        return _.map(this.get('roles'), function(name){
          var role = licor.roles[name];
          return role && role.label;
        }).sort().join(', ');
      }
    }),
    Users = Backbone.Collection.extend({
        model: User
    }),
    Group = Backbone.Model.extend({
      //  defaults: {
      //    model_type: Group,
      //    methods: ['active', 'demo']
      // },
      hasMethod: function(method){
//        return _.contains(this.get('methods'), method);
        return this.get(method);
      },
      renderMethodEdit: function(method, editLabel){
        var out = '<label><input type="checkbox"';
        if(this.hasMethod(method)){
          out += ' checked';
        }
        out += ' value="';
        out += editLabel;
        out += '" name="';
        out += method;
        out += '">';
        out += editLabel;
        out += '</label>';
        return out;
      }
    }),
    Groups = Backbone.Collection.extend({
      model: Group
    }),
    Permission = Backbone.Model.extend({
      defaults: {
        model_type: 'stations',
        methods: ['read', 'subscribe_daily']
      },
      modelName: function(){
        var collection = licor[this.get('model_type')] || {},
            model = collection.get(this.get('model_id'));
        return model ? model.get('name') : '';
      },
      hasMethod: function(method){
        return _.contains(this.get('methods'), method);
      },
      renderMethod: function(method){
        var hasMethod = this.hasMethod(method),
            out = '<img height="20" src="/static/images/';
        if(!hasMethod){
          out += 'no';
        }
        out += 'check.png" class="cstat"><span style="display:none">';
        out += hasMethod ? '0' : '1';
        out += '</span>';

        return out;
      },
      renderMethodEdit: function(method, editLabel){
        var out = '<label><input type="checkbox"';
        if(this.hasMethod(method)){
          out += ' checked';
        }
        out += ' value="';
        out += editLabel;
        out += '" name="';
        out += method;
        out += '">';
        out += editLabel;
        out += '</label>';
        return out;
      }
    }),
    Permissions = Backbone.Collection.extend({
      model: Permission,
      hasMethod: function(modelType, modelId, method){
        var perm = this.findWhere({model_type: modelType, model_id: modelId});
        return perm && perm.hasMethod(method);
      },
      hasPermission: function(modelType, method){
        return !!this.find(function(perm){
          return perm.get('model_type') == modelType && perm.hasMethod(method);
        });
      }
    }),
    FieldDefinition = Backbone.Model.extend({
      superUnits: function(){
        var units = this.get('units');
        if(units){
          units = units.replace(/-?\d+/g, function(match){
            return '<sup>'+match+'</sup>';
          });
        }
        return units;
      }
    }),
    FieldDefinitions = Backbone.Collection.extend({
      model: FieldDefinition
    }),
    // FieldInstrumentMap = Backbone.Model.extend({}),
    // FieldInstrumentMaps = Backbone.Collection.extend({
    //   model: FieldInstrumentMap
    // }),
    InstrumentFieldMap = Backbone.Model.extend({}),
    InstrumentFieldMaps = Backbone.Collection.extend({
      model: InstrumentFieldMap
    }),
    AlertPreset = Backbone.Model.extend({
      superUnits: function(){
        var units = this.get('units');
        if(units){
          units = units.replace(/-?\d+/g, function(match){
            return '<sup>'+match+'</sup>';
          });
        }
        return units;
      }
    }),
    AlertPresets = Backbone.Collection.extend({
      model: AlertPreset
    }),
    AlertSummary = Backbone.Model.extend({}),
    AlertSummaries = Backbone.Collection.extend({
      model: AlertSummary
    }),
    Alert = Backbone.Model.extend({}),
    Alerts = Backbone.Collection.extend({
      model: Alert
    }),
    Instrument = Backbone.Model.extend({
      getOrEmpty: function(prop){
        var val = this.get(prop);
        return _.isEmpty(val) ? '--EMPTY--' : val;
      }
    }),
    Instruments = Backbone.Collection.extend({
      model: Instrument
    }),
    Note = Backbone.Model.extend({
      user: function(){
        if(this.has('create_user_id')){
          var u = licor.users.get(+this.get('create_user_id'));
          if(u && u.has('name')){
            return u.get('name');
          }
        }
        return '';
      }
    }),
    Notes = Backbone.Collection.extend({
      model: Note
    });
licor.stations = new Stations();
licor.User = User;
licor.users = new Users();
licor.permissions = new Permissions();
licor.currentUserPermissions = new Permissions();
licor.fieldDefinitions = new FieldDefinitions();
// licor.fieldInstrumentMap = new FieldInstrumentMap();
// licor.fieldInstrumentMaps = new FieldInstrumentMaps();
licor.instrumentFieldMaps = new InstrumentFieldMaps();
licor.groups = new Groups();
licor.alertPresets = new AlertPresets();
licor.alerts = new Alerts();
licor.alertSummaries = new AlertSummaries();
licor.instruments = new Instruments();
licor.notes = new Notes();
})(this);
