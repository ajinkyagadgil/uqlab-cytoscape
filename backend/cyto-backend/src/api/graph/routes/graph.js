'use strict';

/**
 * graph router.
 */

const { createCoreRouter } = require('@strapi/strapi').factories;

module.exports = createCoreRouter('api::graph.graph');
