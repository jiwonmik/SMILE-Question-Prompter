import axios from 'axios';
import { IReqBody } from 'types/api.type';

const BASE_URL = 'https://www.smile-similarity.org/smile/similarity/question';

export const getSpacyRes = async (input: IReqBody) => {
  const response = await axios.post(`${BASE_URL}`, input);
  return response;
};

export const getSpacyKorRes = async (input: IReqBody) => {
  const response = await axios.post(`${BASE_URL}/korean`, input);
  return response;
};

export const getOpenAIRes = async (input: IReqBody) => {
  const response = await axios.post(`${BASE_URL}/gpt`, input);
  return response;
};
