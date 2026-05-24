import { router } from 'expo-router';
import { useEffect } from 'react';
import { Image, StyleSheet, Text, View } from 'react-native';
import { Colors } from '../constants/Colors';

export default function SplashScreen() {
  useEffect(() => {
    const timer = setTimeout(() => {
      router.replace('/onboarding/one');
    }, 4000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <View style={styles.container}>
      <Image
        source={require('../assets/images/canola_flower_main.png')}
        style={styles.flower}
      />
      <Text style={styles.title}>월동</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.pageBg,
    alignItems: 'center',
    justifyContent: 'center',
  },
  flower: {
    width: 180,
    height: 180,
    marginBottom: 16,
  },
  title: {
    fontFamily: 'EastSeaDokdo_400Regular',
    fontSize: 80,
    color: Colors.text,
  },
});