export interface Input {
  question: string;
  keywords: string;
}

interface SimilarityInfo {
  question_token: string;
  similarity: number;
}

interface KeywordResInfo {
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
