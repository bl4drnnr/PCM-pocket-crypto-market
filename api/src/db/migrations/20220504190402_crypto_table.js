/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function(knex) {
  return knex.schema.createTable("crypto", t => {
      t.uuid("id").primary().notNullable()
      t.string("symbol")
      t.float("mark_price")
      t.float("index_price")
      t.float("bid_price")
      t.float("ask_price")
      t.float("high_price_24h")
      t.float("low_price_24h")
      t.timestamp('createdAt').defaultTo(knex.fn.now())
      t.timestamp('updatedAt').defaultTo(knex.fn.now())
  })
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function(knex) {
  return knex.schema.dropTable("crypto");
};
