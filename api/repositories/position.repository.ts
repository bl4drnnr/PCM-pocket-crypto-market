const knex = require("../src/db/knex.js");
const uuid = require("uuid");
import { Position } from "../interfaces/position.interface";

export const getUserPositionsById = async (id: string) => {
    return await knex('positions').where("id", id).first();
};

export const createPosition = async (position: Position) => {
    return await knex('positions').insert(position);
};

export const updatePosition = async (position: Position) => {
    return await knex('positions').update(position).where("id", position.id);
};

export const deletePosition = async (position: Position) => {
    return await knex('positions').del().where("id", position.id);
};