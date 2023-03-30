import {
  Textarea,
  Button,
  Tag,
  TagLabel,
  HStack,
  Input,
  TagCloseButton,
  SimpleGrid,
} from '@chakra-ui/react';
import { useState } from 'react';
import { IInput, IReqBody, IValidityRes } from 'types/api.type';
import { getSpacyRes, getSpacyKorRes, getOpenAIRes } from 'api/api';
import { PrompterProps } from 'types/type';
import SimilarityList from './SimilarityList';

function Prompter({ option }: PrompterProps) {
  const InitialInput = {
    question: '',
    keyword: '',
  };
  const [input, setInput] = useState<IInput>(InitialInput);
  const [keywords, setKeywords] = useState<string[]>([]);

  const onAddHandle = () => {
    setKeywords((prev) => {
      return [...prev, ...input.keyword.replace(' ', '').split(',')];
    });
    setInput((prev) => {
      return { ...prev, keyword: '' };
    });
  };
  const onResetHandle = () => {
    setKeywords(() => {
      return [];
    });
  };

  const onDeleteHandle = (index: number) => {
    setKeywords((prev) => {
      return [...prev.slice(0, index), ...prev.slice(index + 1)];
    });
  };

  const [validityRes, setValidityRes] = useState<IValidityRes>();

  const questionPlaceholder =
    option === 'eng'
      ? 'ex. How many people had gone through the computer training?'
      : 'ex. 소리 파형을 측정할 때, 종파를 구분하려면, 어떤 측정기가 필요할까요?';
  const keywordsPlaceholder = option === 'eng' ? 'ex. Individuals, computers' : 'ex. 파형, 필요';

  const onSpacyCheck = () => {
    const body = {
      question: input?.question,
      keywords: keywords.join(', '),
    } as IReqBody;
    switch (option) {
      case 'eng': {
        getSpacyRes(body).then((res) => {
          setValidityRes(() => {
            return {
              question: res?.data.question,
              valid: res?.data.valid,
              keywords_result: res?.data.keywords_result,
            };
          });
        });
        break;
      }
      case 'kor': {
        getSpacyKorRes(body).then((res) => {
          setValidityRes(() => {
            return {
              question: res?.data.question,
              valid: res?.data.valid,
              keywords_result: res?.data.keywords_result,
            };
          });
        });
      }
    }
  };

  const onOpenAICheck = () => {
    const body = {
      question: input?.question,
      keywords: keywords.join(', '),
    } as IReqBody;
    getOpenAIRes(body).then((res) => {
      setValidityRes(() => {
        return {
          question: res?.data.question,
          valid: res?.data.valid,
          gpt_response: res?.data.gpt_response,
        };
      });
    });
  };

  return (
    <>
      <HStack mb="5">
        <Input
          value={input?.keyword}
          onChange={(e) =>
            setInput((prev) => {
              return { ...prev, keyword: e.target.value };
            })
          }
          placeholder={keywordsPlaceholder}
          resize={'none'}
        />
        <Button onClick={onAddHandle}>Add</Button>
        <Button onClick={onResetHandle}>Reset</Button>
      </HStack>
      <SimpleGrid columns={3} spacing={5} mb="5">
        {keywords.map((keyword, index) => (
          <Tag key={index} size="lg" colorScheme={'red'} borderRadius="full" width={'fit-content'}>
            <TagLabel>{keyword}</TagLabel>
            <TagCloseButton onClick={() => onDeleteHandle(index)} />
          </Tag>
        ))}
      </SimpleGrid>
      <Textarea
        value={input?.question}
        onChange={(e) =>
          setInput((prev) => {
            return { ...prev, question: e.target.value };
          })
        }
        my={5}
        placeholder={questionPlaceholder}
        width="full"
        height="100px"
        resize={'none'}
      />
      <Button onClick={onSpacyCheck} colorScheme={'blue'} width="full">
        Check with spaCy
      </Button>
      <Button onClick={onOpenAICheck} colorScheme={'red'} width="full" my={5}>
        Check with OpenAI
      </Button>

      <SimilarityList
        question={validityRes?.question}
        valid={validityRes?.valid}
        keywords_result={validityRes?.keywords_result}
        gpt_response={validityRes?.gpt_response}
      />
    </>
  );
}

export default Prompter;
