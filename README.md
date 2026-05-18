# Real-Time Fraud Analysis Pipeline: Redis Streams to Databricks Delta Lake

## 📌 Project Overview
This project implements an end-to-end, real-time data streaming pipeline designed for financial fraud analysis. It simulates a distributed corporate system where a local transaction processing application continuously generates mock credit card transactions and streams them to a cloud-hosted event broker using **Redis Streams (Upstash)**. 

A multi-cloud **Databricks** instance consumes the live stream via Spark Structured Streaming, enforces data schemas, captures unexpected structural anomalies using the **Quarantine Pattern**, evaluates transactions for fraudulent behavior on the fly, and appends optimized records into a **Delta Lake** Lakehouse architecture.

### Key Highlights & Architecture Patterns
*   **Zero Local Broker Overhead:** Uses cloud-managed Redis Streams to simulate lightweight, real-time Kafka broker mechanics without local installations.
*   **SLA Protection (The Quarantine Pattern):** Upstream schema changes or corrupted payloads are isolated at the ingestion layer into a rescued metadata schema, ensuring downstream BI dashboards experience **zero downtime**.
*   **Incremental Processing:** Built using Spark Structured Streaming to scale boundlessly with micro-batching.
*   **Delta Lake Optimization:** Enforces ACID transactions, enables data time-travel, and leverages high-performance storage layouts.

---

## 🏗️ Technical Architecture

```text
[ Local Python App ] 
       │ (Generates live transactions & simulated fraud anomalies)
       ▼
[ Upstash Redis Cloud ] ---> (Redis Streams / Append-only event log)
       │
       ▼  (Spark Structured Streaming via Spark-Redis Connector)
[ Databricks Engine ]
       │
       ├───► [ Schema Validation Check ] 
       │         │
       │         ├──► Anomaly Detected ──► [ Isolate in Bronze Rescued Column ] ──► [ Alerting Engine ]
       │         └──► Valid Schema     ──► [ Extract & Cast Properties ]
       ▼
[ Delta Lake Storage ] ---> [ Bronze Table ] ──► [ Silver/Gold Layers ] ──► [ Live BI Dashboards ]
