import { config } from '@gluestack-ui/config';
import { Box, ButtonText, GluestackUIProvider, Heading, InputField, Text, VStack, Button, Input } from '@gluestack-ui/themed';
import { ScrollView } from 'react-native';
import Gradient from './assets/Icons/Gradient';
import DocumentData from './assets/Icons/DocumentData';
import LightBulbPerson from './assets/Icons/LightbulbPerson';
import Rocket from './assets/Icons/Rocket';
import Logo from './assets/Icons/Logo';
import { SetStateAction, useState } from 'react';
export default function App() {
  return (
    <GluestackUIProvider config={config}>
      <Home />
    </GluestackUIProvider>
  );
}
const Home = () => {
  return <Container />;
};
const Container = () => {
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [summary, setSummary] = useState('');

  const handleInputChange = (text: SetStateAction<string>) => {
    setYoutubeUrl(text);
  };

  const handleButtonClick = async () => {
    if (youtubeUrl.trim() === '') {
      alert('Please enter a YouTube URL');
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch('https://backend-5q2auqtn5a-og.a.run.app/api/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ youtube_video_url: youtubeUrl }),
      });

      if (!response.ok) {
        setIsLoading(false);
        alert('Failed to summarize video');
        return;
      }

      const data = await response.json();
      setSummary(data.summary);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box flex={1}>
      <ScrollView
        style={{
          height: '100%',
        }}
        contentContainerStyle={{
          flexGrow: 1,
        }}
      >
        <Box
          height="100%"
          $base-my="$16"
          $base-mx="$5"
          $base-h="80%"
          $lg-my="$24"
          $lg-mx="$32"
        >
          <Box
            p="$5"
            maxWidth="$96"
            borderWidth="$1"
            borderColor="$backgroundLight300"
            borderRadius="$lg"
            $dark-borderColor="$backgroundDark700"
          >
            <VStack space="xs" pb="$4">
              <Heading lineHeight={30}>YouTube Summary</Heading>
            </VStack>
            <VStack space="xl" py="$2">
              <Input>
                <InputField py="$2" placeholder="Just insert a YouTube link" value={youtubeUrl} onChangeText={handleInputChange} />
              </Input>
            </VStack>
            <VStack space="lg" pt="$4">
              <Button size="sm" onPress={handleButtonClick} disabled={isLoading}>
                <ButtonText>{isLoading ? 'Loading...' : 'GO'}</ButtonText>
              </Button>
            </VStack>
          </Box>
          {summary ? (
            <Box
              marginTop="$3"
              p="$5"
              maxWidth="$96"
              borderWidth="$1"
              borderColor="$backgroundLight300"
              borderRadius="$lg"
              $dark-borderColor="$backgroundDark700">
              <Text>{summary}</Text>
            </Box>
          ) : null}
        </Box>
      </ScrollView>
    </Box>
  );
};
