import React, { useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import { useQuery } from '@tanstack/react-query';
import { statsApi } from '@/lib/api/stats';
import { LineChart, PieChart } from 'react-native-chart-kit';
import { format, subDays } from 'date-fns';

const screenWidth = Dimensions.get('window').width;

export default function FinanceScreen() {
  const endDate = new Date();
  const startDate = subDays(endDate, 30);

  const { data: dailyStats, isLoading: isDailyLoading } = useQuery({
    queryKey: ['stats', 'daily'],
    queryFn: () =>
      statsApi.daily({
        start_date: format(startDate, 'yyyy-MM-dd'),
        end_date: format(endDate, 'yyyy-MM-dd'),
      }),
  });

  const { data: monthlyStats, isLoading: isMonthlyLoading } = useQuery({
    queryKey: ['stats', 'monthly'],
    queryFn: () => statsApi.monthly(),
  });

  const { data: categoryStats, isLoading: isCategoryLoading } = useQuery({
    queryKey: ['stats', 'category'],
    queryFn: () => statsApi.category({ transaction_type: 'expense' }),
  });

  if (isDailyLoading || isMonthlyLoading || isCategoryLoading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  // 최근 30일 지출 데이터
  const expenseData = dailyStats?.map((stat) => parseFloat(stat.total_expense.toString())) || [];
  const maxExpense = Math.max(...expenseData, 0);

  // 이번 달 통계
  const thisMonth = monthlyStats?.[0];
  const totalIncome = thisMonth ? parseFloat(thisMonth.total_income.toString()) : 0;
  const totalExpense = thisMonth ? parseFloat(thisMonth.total_expense.toString()) : 0;
  const net = totalIncome - totalExpense;

  // 카테고리별 파이 차트 데이터
  const pieData =
    categoryStats?.slice(0, 5).map((stat, index) => ({
      name: stat.category,
      amount: parseFloat(stat.total_amount.toString()),
      color: [
        '#FF6384',
        '#36A2EB',
        '#FFCE56',
        '#4BC0C0',
        '#9966FF',
      ][index % 5],
      legendFontColor: '#333',
      legendFontSize: 14,
    })) || [];

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>경제 현황</Text>
        <Text style={styles.headerSubtitle}>
          {format(new Date(), 'yyyy년 MM월')}
        </Text>
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        {/* 이번 달 요약 */}
        <View style={styles.summaryCard}>
          <View style={styles.summaryRow}>
            <View style={styles.summaryItem}>
              <Text style={styles.summaryLabel}>수입</Text>
              <Text style={[styles.summaryValue, styles.incomeColor]}>
                +{totalIncome.toLocaleString()}원
              </Text>
            </View>
            <View style={styles.summaryItem}>
              <Text style={styles.summaryLabel}>지출</Text>
              <Text style={[styles.summaryValue, styles.expenseColor]}>
                -{totalExpense.toLocaleString()}원
              </Text>
            </View>
          </View>
          <View style={styles.summaryDivider} />
          <View style={styles.summaryItem}>
            <Text style={styles.summaryLabel}>순수익</Text>
            <Text
              style={[
                styles.summaryValueLarge,
                net >= 0 ? styles.incomeColor : styles.expenseColor,
              ]}
            >
              {net >= 0 ? '+' : ''}
              {net.toLocaleString()}원
            </Text>
          </View>
        </View>

        {/* 최근 30일 지출 추이 */}
        {expenseData.length > 0 && maxExpense > 0 && (
          <View style={styles.chartCard}>
            <Text style={styles.chartTitle}>최근 30일 지출 추이</Text>
            <LineChart
              data={{
                labels: [],
                datasets: [
                  {
                    data: expenseData.length > 0 ? expenseData : [0],
                  },
                ],
              }}
              width={screenWidth - 64}
              height={200}
              chartConfig={{
                backgroundColor: '#fff',
                backgroundGradientFrom: '#fff',
                backgroundGradientTo: '#fff',
                decimalPlaces: 0,
                color: (opacity = 1) => `rgba(255, 59, 48, ${opacity})`,
                labelColor: (opacity = 1) => `rgba(102, 102, 102, ${opacity})`,
                style: {
                  borderRadius: 16,
                },
                propsForDots: {
                  r: '3',
                  strokeWidth: '2',
                  stroke: '#ff3b30',
                },
              }}
              bezier
              style={styles.chart}
              withHorizontalLabels={true}
              withVerticalLabels={false}
              withInnerLines={false}
              withOuterLines={true}
            />
          </View>
        )}

        {/* 카테고리별 지출 */}
        {pieData.length > 0 && (
          <View style={styles.chartCard}>
            <Text style={styles.chartTitle}>카테고리별 지출</Text>
            <PieChart
              data={pieData}
              width={screenWidth - 64}
              height={220}
              chartConfig={{
                color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
              }}
              accessor="amount"
              backgroundColor="transparent"
              paddingLeft="15"
              absolute
            />
          </View>
        )}

        {/* 카테고리별 상세 */}
        {categoryStats && categoryStats.length > 0 && (
          <View style={styles.categoryCard}>
            <Text style={styles.chartTitle}>카테고리 상세</Text>
            {categoryStats.slice(0, 5).map((stat, index) => (
              <View key={index} style={styles.categoryItem}>
                <View style={styles.categoryLeft}>
                  <View
                    style={[
                      styles.categoryDot,
                      {
                        backgroundColor: [
                          '#FF6384',
                          '#36A2EB',
                          '#FFCE56',
                          '#4BC0C0',
                          '#9966FF',
                        ][index % 5],
                      },
                    ]}
                  />
                  <Text style={styles.categoryName}>{stat.category}</Text>
                </View>
                <View style={styles.categoryRight}>
                  <Text style={styles.categoryAmount}>
                    {parseFloat(stat.total_amount.toString()).toLocaleString()}원
                  </Text>
                  <Text style={styles.categoryPercentage}>
                    {stat.percentage.toFixed(1)}%
                  </Text>
                </View>
              </View>
            ))}
          </View>
        )}

        {/* 빈 상태 */}
        {(!dailyStats || dailyStats.length === 0) &&
          (!categoryStats || categoryStats.length === 0) && (
            <View style={styles.emptyContainer}>
              <Text style={styles.emptyText}>아직 거래 내역이 없습니다</Text>
              <Text style={styles.emptySubtext}>
                홈 탭에서 지출/수입을 기록해보세요
              </Text>
            </View>
          )}

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
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
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
  headerSubtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  content: {
    flex: 1,
    padding: 16,
  },
  summaryCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  summaryRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 20,
  },
  summaryItem: {
    alignItems: 'center',
  },
  summaryLabel: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  summaryValue: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  summaryValueLarge: {
    fontSize: 28,
    fontWeight: 'bold',
  },
  incomeColor: {
    color: '#34c759',
  },
  expenseColor: {
    color: '#ff3b30',
  },
  summaryDivider: {
    height: 1,
    backgroundColor: '#e0e0e0',
    marginVertical: 20,
  },
  chartCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  chartTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 16,
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
  categoryCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  categoryItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  categoryLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  categoryDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
  },
  categoryName: {
    fontSize: 15,
    color: '#333',
    fontWeight: '500',
  },
  categoryRight: {
    alignItems: 'flex-end',
  },
  categoryAmount: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 2,
  },
  categoryPercentage: {
    fontSize: 12,
    color: '#666',
  },
  emptyContainer: {
    alignItems: 'center',
    paddingTop: 80,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#666',
    marginBottom: 8,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#999',
  },
});

