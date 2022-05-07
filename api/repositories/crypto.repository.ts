const knex = require("../src/db/knex.js");
const uuid = require("uuid");

export const getAllPairs = async () => {
    return await knex('crypto').select('*');
}

export const getPair = async (pair: string) => {
    return await knex('crypto').where("pair", pair).first();
}

export const updateRates = async (data: object) => {
    await knex('crypto').del('*')
    return await knex('crypto').insert({...data, id: uuid.v4()});
};
