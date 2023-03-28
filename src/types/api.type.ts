export interface IInput {
  question: string;
  keyword: string;
}

export interface IReqBody {
  question: string;
  keywords: string;
}

interface SimilarityInfo {
  question_token: string;
  similarity: number;
}

interface KeywordResInfo {
  identical: string[];
  included: SimilarityInfo[];
  not_included: SimilarityInfo[];
}

interface KeywordRes {
  keyword: string;
  result: KeywordResInfo;
}

export interface SimilarityRes {
  question: string;
  valid: boolean;
  keywords_result: KeywordRes[];
}
