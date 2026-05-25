import { Pressable, StyleSheet, Text } from 'react-native';
import { Colors } from '../constants/Colors';

type Props = {
  label: string;
  onPress: () => void;
};

export default function PrimaryButton({ label, onPress }: Props) {
  return (
    <Pressable style={styles.button} onPress={onPress}>
      <Text style={styles.text}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    width: '82%',
    height: 52,
    borderRadius: 30,
    backgroundColor: Colors.highlight1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    fontFamily: 'Sumana_700Bold',
    fontSize: 20,
    color: Colors.text,
  },
});