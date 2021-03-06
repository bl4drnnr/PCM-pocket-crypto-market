const knex = require("../src/db/knex.js");
import { IVoucher } from "../interfaces/voucher.interface";

export const getVoucher = async (codeenc: string) => {
    return await knex("vouchers").where("codeenc", codeenc).first()
};

export const getVouchersByClientId = async (userid: string) => {
    return await knex("vouchers")
        .where("userid", userid)
        .leftJoin("crypto", "crypto.id", "vouchers.currencyid")
        .select("vouchers.amount", "vouchers.userid", "vouchers.codeenc", "vouchers.createdat", "crypto.symbol")
};

export const generateVoucher = async (voucher: IVoucher) => {
    return await knex("vouchers").insert(voucher)
};

export const redeemVoucher = async () => {

};
