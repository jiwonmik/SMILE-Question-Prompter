import { IValidityRes } from 'types/api.type';
import { Text, Box, Alert, AlertIcon, Divider, Heading } from '@chakra-ui/react';

function SimilarityList({ question, valid, keywords_result, gpt_response }: IValidityRes) {
  return question !== undefined ? (
    <>
      <Box borderRadius={'md'} bg="gray.100" padding={'5'} mb={'5'}>
        <Text>Your question: {question}</Text>
      </Box>
      {valid ? (
        <Alert status="success" mb="5">
          <AlertIcon />
          Valid Question
        </Alert>
      ) : (
        <Alert status="error" mb="5">
          <AlertIcon />
          Unvalid Question
        </Alert>
      )}
      <Divider colorScheme={'blue'} mb="5" />
      {keywords_result !== undefined ? (
        keywords_result.map((res, index) =>
          res.result.identical.length + res.result.included.length == 0 ? (
            <Box key={index} borderRadius={'md'} bg="red.100" padding={'5'} mb={'5'}>
              <Text>Keyword &apos;{res.keyword}&apos; is not included</Text>
            </Box>
          ) : res.result.identical.length !== 0 ? (
            <Box key={index} borderRadius={'md'} bg="yellow.100" padding={'5'} mb={'5'}>
              <Text>Keyword: {res.result.identical}</Text>
              <Text>similarity: identical word</Text>
            </Box>
          ) : (
            <Box key={index} borderRadius={'md'} bg="green.100" padding={'5'} mb={'5'}>
              <Text>Keyword: {res.keyword}</Text>
              {res.result.included.map((res, index) => (
                <>
                  <Text key={index}>question token: {res.question_token} </Text>
                  <Text>similarity: {res.similarity}</Text>
                </>
              ))}
            </Box>
          )
        )
      ) : gpt_response !== undefined ? (
        <Box borderRadius={'md'} bg="red.100" padding={'5'} mb={'5'}>
          <Heading size="md" mb="3">
            GPT Response
          </Heading>
          <Text>{gpt_response}</Text>
        </Box>
      ) : null}
    </>
  ) : null;
}

export default SimilarityList;
