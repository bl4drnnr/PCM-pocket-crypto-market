import { Knex, knex } from 'knex'
import dotenv from "dotenv";
import path from "path";

dotenv.config({
    path: path.resolve(path.resolve(), "../.env")
})

const knexConfig: Knex.Config = {
    client: 'mysql',
    connection: {
        host: process.env.DATABASE_HOST,
        user: process.env.DATABASE_USERNAME,
        password: process.env.DATABASE_PASSWORD,
        database: process.env.DATABASE_DATABASE,
    },
    migrations: {
        tableName: 'knex_migrations',
        directory: __dirname + './migrations'
    },
    seeds: {
        directory: __dirname + './seeders'
    },
    debug: false
};

const knexInstanse = knex(knexConfig);

export default knexInstanse;