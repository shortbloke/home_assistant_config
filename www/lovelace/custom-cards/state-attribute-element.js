// Source: https://github.com/custom-cards/state-attribute-element
class StateAttributeElement extends HTMLElement {
    set hass(hass) {
      const entityId = this.config.entity;
      const attr = this.config.attribute;
      const state = hass.states[entityId].attributes[attr];
      const card = document.createElement('state-attribute-element');
      this.innerHTML = state;
    }
    setConfig(config) {
      if (!config.entity) {
        throw new Error('You need to define an entity');
      }
      if (!config.attribute) {
        throw new Error('You need to define an attribute');
      }
      this.config = config;
    }
  
    getCardSize() {
      return 1;
    }
  }
  customElements.define('state-attribute-element', StateAttributeElement);