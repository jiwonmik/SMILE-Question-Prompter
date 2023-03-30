export interface IInput {
  question: string;
  keyword: string;
}

export interface IReqBody {
  question: string;
  keywords: string;
}

interface SpacyResInfo {
  question_token: string;
  similarity: number;
}

interface KeywordResInfo {
  identical: string[];
  included: SpacyResInfo[];
  not_included: SpacyResInfo[];
}

interface KeywordRes {
  keyword: string;
  result: KeywordResInfo;
}

export interface IValidityRes {
  question?: string;
  valid?: boolean;
  keywords_result?: KeywordRes[];
  gpt_response?: string;
}
