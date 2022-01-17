'use strict';

/**
 * graph service.
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::graph.graph');
