import axios from 'axios';
import { Input } from 'types/type';

const BASE_URL = 'http://45.32.89.216/similarity';

export const fetchData = async (input: Input) => {
  const response = await axios.post(`${BASE_URL}/question`, input);
  
  return response;
};
