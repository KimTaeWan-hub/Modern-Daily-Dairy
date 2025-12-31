import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { useRouter } from 'expo-router';
import { format } from 'date-fns';
import { entriesApi } from '@/lib/api/entries';
import { TransactionType } from '@/lib/types';

const MOODS = ['😊', '😢', '😐', '😃', '😴', '😤'];
const CATEGORIES = ['식비', '교통비', '쇼핑', '문화생활', '기타', '급여', '용돈'];

interface TransactionInput {
  type: TransactionType;
  category: string;
  amount: string;
  description: string;
}

export default function HomeScreen() {
  const router = useRouter();
  const [date] = useState(new Date());
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [mood, setMood] = useState('');
  const [transactions, setTransactions] = useState<TransactionInput[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const addTransaction = () => {
    setTransactions([
      ...transactions,
      { type: 'expense', category: '식비', amount: '', description: '' },
    ]);
  };

  const updateTransaction = (index: number, field: keyof TransactionInput, value: string) => {
    const updated = [...transactions];
    updated[index] = { ...updated[index], [field]: value };
    setTransactions(updated);
  };

  const removeTransaction = (index: number) => {
    setTransactions(transactions.filter((_, i) => i !== index));
  };

  const handleSave = async () => {
    if (!content && transactions.length === 0) {
      Alert.alert('오류', '일기 내용이나 거래 내역 중 하나는 입력해야 합니다.');
      return;
    }

    setIsLoading(true);
    try {
      const validTransactions = transactions
        .filter((t) => t.amount && parseFloat(t.amount) > 0)
        .map((t) => ({
          date: format(date, 'yyyy-MM-dd'),
          type: t.type,
          category: t.category,
          amount: parseFloat(t.amount),
          description: t.description || undefined,
        }));

      await entriesApi.createWithTransactions({
        entry: {
          date: format(date, 'yyyy-MM-dd'),
          title: title || undefined,
          content: content || undefined,
          mood: mood || undefined,
          photos: [],
          tags: [],
        },
        transactions: validTransactions,
      });

      Alert.alert('성공', '기록이 저장되었습니다.', [
        {
          text: '확인',
          onPress: () => {
            setTitle('');
            setContent('');
            setMood('');
            setTransactions([]);
            router.push('/(tabs)/timeline');
          },
        },
      ]);
    } catch (error: any) {
      Alert.alert('오류', error.response?.data?.detail || '저장에 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>오늘의 기록</Text>
        <Text style={styles.headerDate}>{format(date, 'yyyy년 MM월 dd일')}</Text>
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        {/* 제목 */}
        <TextInput
          style={styles.titleInput}
          placeholder="제목 (선택사항)"
          value={title}
          onChangeText={setTitle}
          editable={!isLoading}
        />

        {/* 감정 선택 */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>오늘의 기분</Text>
          <View style={styles.moodContainer}>
            {MOODS.map((emoji) => (
              <TouchableOpacity
                key={emoji}
                style={[styles.moodButton, mood === emoji && styles.moodButtonSelected]}
                onPress={() => setMood(emoji)}
                disabled={isLoading}
              >
                <Text style={styles.moodEmoji}>{emoji}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* 일기 내용 */}
        <TextInput
          style={styles.contentInput}
          placeholder="오늘 하루는 어땠나요?"
          value={content}
          onChangeText={setContent}
          multiline
          numberOfLines={6}
          textAlignVertical="top"
          editable={!isLoading}
        />

        {/* 거래 내역 */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>오늘의 지출/수입</Text>
            <TouchableOpacity
              style={styles.addButton}
              onPress={addTransaction}
              disabled={isLoading}
            >
              <Text style={styles.addButtonText}>+ 추가</Text>
            </TouchableOpacity>
          </View>

          {transactions.map((transaction, index) => (
            <View key={index} style={styles.transactionCard}>
              <View style={styles.transactionRow}>
                <TouchableOpacity
                  style={[
                    styles.typeButton,
                    transaction.type === 'expense' && styles.typeButtonExpense,
                    transaction.type === 'income' && styles.typeButtonIncome,
                  ]}
                  onPress={() =>
                    updateTransaction(
                      index,
                      'type',
                      transaction.type === 'expense' ? 'income' : 'expense'
                    )
                  }
                  disabled={isLoading}
                >
                  <Text style={styles.typeButtonText}>
                    {transaction.type === 'expense' ? '지출' : '수입'}
                  </Text>
                </TouchableOpacity>

                <TextInput
                  style={styles.categoryInput}
                  placeholder="카테고리"
                  value={transaction.category}
                  onChangeText={(value) => updateTransaction(index, 'category', value)}
                  editable={!isLoading}
                />

                <TouchableOpacity
                  style={styles.deleteButton}
                  onPress={() => removeTransaction(index)}
                  disabled={isLoading}
                >
                  <Text style={styles.deleteButtonText}>✕</Text>
                </TouchableOpacity>
              </View>

              <TextInput
                style={styles.amountInput}
                placeholder="금액"
                value={transaction.amount}
                onChangeText={(value) => updateTransaction(index, 'amount', value)}
                keyboardType="numeric"
                editable={!isLoading}
              />

              <TextInput
                style={styles.descriptionInput}
                placeholder="메모 (선택사항)"
                value={transaction.description}
                onChangeText={(value) => updateTransaction(index, 'description', value)}
                editable={!isLoading}
              />
            </View>
          ))}
        </View>

        {/* 저장 버튼 */}
        <TouchableOpacity
          style={[styles.saveButton, isLoading && styles.saveButtonDisabled]}
          onPress={handleSave}
          disabled={isLoading}
        >
          {isLoading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.saveButtonText}>저장하기</Text>
          )}
        </TouchableOpacity>

        <View style={{ height: 40 }} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    backgroundColor: '#fff',
    padding: 20,
    paddingTop: 60,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  headerDate: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  content: {
    flex: 1,
    padding: 20,
  },
  titleInput: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  section: {
    marginBottom: 24,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 12,
  },
  moodContainer: {
    flexDirection: 'row',
    gap: 12,
  },
  moodButton: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#e0e0e0',
  },
  moodButtonSelected: {
    borderColor: '#007AFF',
    backgroundColor: '#e7f3ff',
  },
  moodEmoji: {
    fontSize: 28,
  },
  contentInput: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    fontSize: 16,
    marginBottom: 24,
    minHeight: 150,
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  addButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
  },
  addButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  transactionCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  transactionRow: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 12,
    alignItems: 'center',
  },
  typeButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
  },
  typeButtonExpense: {
    backgroundColor: '#ff3b30',
  },
  typeButtonIncome: {
    backgroundColor: '#34c759',
  },
  typeButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  categoryInput: {
    flex: 1,
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    padding: 10,
    fontSize: 14,
  },
  deleteButton: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#ff3b30',
    justifyContent: 'center',
    alignItems: 'center',
  },
  deleteButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  amountInput: {
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
  },
  descriptionInput: {
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    padding: 12,
    fontSize: 14,
  },
  saveButton: {
    backgroundColor: '#007AFF',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    marginTop: 16,
  },
  saveButtonDisabled: {
    opacity: 0.6,
  },
  saveButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
