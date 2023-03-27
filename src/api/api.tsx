import axios from 'axios';
import { Input } from 'types/api.type';

const BASE_URL = 'http://45.32.89.216/similarity/question';

export const fetchData = async (input: Input) => {
  const response = await axios.post(`${BASE_URL}`, input);
  return response;
};

export const fetchKorData = async (input: Input) => {
  const response = await axios.post(`${BASE_URL}/korean`, input);
  return response;
};
