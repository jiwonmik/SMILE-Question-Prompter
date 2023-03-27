import { Textarea, Button, Text, Box, Alert, AlertIcon } from '@chakra-ui/react';
import { useState } from 'react';
import { Input, SimilarityRes } from 'types/api.type';
import { fetchData, fetchKorData } from 'api/api';
import { PrompterProps } from 'types/type';

function Prompter({ option }: PrompterProps) {
  const InitialInput = {
    question: '',
    keywords: '',
  };
  const [input, setInput] = useState<Input>(InitialInput);
  const [similairty, setSimilarity] = useState<SimilarityRes>();
  const questionPlaceholder =
    option === 'eng'
      ? 'ex. How many people had gone through the computer training?'
      : 'ex. 소리 파형을 측정할 때, 종파를 구분하려면, 어떤 측정기가 필요할까요?';
  const keywordsPlaceholder = option === 'eng' ? 'ex. Individuals, computers' : 'ex. 파형, 필요';

  const OnCheckHandle = () => {
    switch (option) {
      case 'eng': {
        fetchData(input).then((res) => {
          setSimilarity(() => {
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
        fetchKorData(input).then((res) => {
          console.log(res.data);
          setSimilarity(() => {
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

  return (
    <>
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
        height="170px"
        resize={'none'}
      />
      <Textarea
        value={input?.keywords}
        onChange={(e) =>
          setInput((prev) => {
            return { ...prev, keywords: e.target.value };
          })
        }
        placeholder={keywordsPlaceholder}
        width="full"
        height="100px"
        resize={'none'}
      />
      <Button onClick={OnCheckHandle} colorScheme={'red'} width="full" my={5}>
        Check
      </Button>
      {similairty?.question !== undefined ? (
        <>
          <Box borderRadius={'md'} bg="red.100" padding={'5'} mb={'5'}>
            <Text>Your question: {similairty?.question}</Text>
            <Text>Your keywords: {input.keywords}</Text>
          </Box>
          {similairty?.valid ? (
            <Alert status="success">
              <AlertIcon />
              Valid
            </Alert>
          ) : (
            <Alert status="error">
              <AlertIcon />
              Unvalid
            </Alert>
          )}
        </>
      ) : null}
    </>
  );
}

export default Prompter;
