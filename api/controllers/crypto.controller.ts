import { Request, Response } from "express";
import * as cryptoService from "../services/crypto.service";
import loggerConfig from "../common/logger";

const logger = loggerConfig({ label: 'crypto-controller', path: 'crypto' })

export const getPair = async (req: Request, res: Response) => {
    try {
        const result = await cryptoService.getPair(req.params.pair);
        return res.json(result);
    } catch (e) {
        logger.error(`Error while getting pair => ${e}`);
        return res.json({ status: -1 });
    }
};

export const updateRates = async (req: Request, res: Response) => {
    try {
        await cryptoService.updateRates(JSON.parse(req.body.updatedPairs));
        return res.json({ status: 1 });
    } catch (e) {
        logger.error(`Error in updating rates => ${e}`);
        return res.json({ status: -1 });
    }
};

export const buyCrypto = async (req: Request, res: Response) => {
    try {

    } catch (e) {
        logger.error(`Error while buying crypto => ${e}`);
        return res.json({ status: -1 });
    }
};

export const sellCrypto = async (req: Request, res: Response) => {
    try {

    } catch (e) {
        logger.error(`Error while selling crypto => ${e}`);
        return res.json({ status: -1 });
    }
};
