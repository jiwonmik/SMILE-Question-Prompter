import {
  Textarea,
  Button,
  Text,
  Box,
  Alert,
  AlertIcon,
  Tag,
  TagLabel,
  HStack,
  Input,
  Grid,
  TagCloseButton,
} from '@chakra-ui/react';
import { useState } from 'react';
import { IInput, IReqBody, SimilarityRes } from 'types/api.type';
import { fetchData, fetchKorData } from 'api/api';
import { PrompterProps } from 'types/type';

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

  const [similairty, setSimilarity] = useState<SimilarityRes>();
  const questionPlaceholder =
    option === 'eng'
      ? 'ex. How many people had gone through the computer training?'
      : 'ex. 소리 파형을 측정할 때, 종파를 구분하려면, 어떤 측정기가 필요할까요?';
  const keywordsPlaceholder = option === 'eng' ? 'ex. Individuals, computers' : 'ex. 파형, 필요';

  const OnCheckHandle = () => {
    const body = {
      question: input?.question,
      keywords: keywords.join(', '),
    } as IReqBody;
    switch (option) {
      case 'eng': {
        fetchData(body).then((res) => {
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
        fetchKorData(body).then((res) => {
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
      <Grid templateColumns="repeat(4, 1fr)" gap={5} mb="5">
        {keywords.map((keyword, index) => (
          <Tag key={index} size="lg" colorScheme={'red'} borderRadius="full" width={'fit-content'}>
            <TagLabel>{keyword}</TagLabel>
            <TagCloseButton onClick={() => onDeleteHandle(index)} />
          </Tag>
        ))}
      </Grid>
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
      <Button onClick={OnCheckHandle} colorScheme={'red'} width="full" my={5}>
        Check
      </Button>
      {similairty?.question !== undefined ? (
        <>
          <Box borderRadius={'md'} bg="red.100" padding={'5'} mb={'5'}>
            <Text>Your question: {similairty?.question}</Text>
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
