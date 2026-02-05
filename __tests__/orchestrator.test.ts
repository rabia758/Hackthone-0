import { Orchestrator } from '../src/orchestrator/Orchestrator';
import { Config } from '../src/types/task.types';

describe('Orchestrator', () => {
  let orchestrator: Orchestrator;
  let config: Config;

  beforeEach(() => {
    config = {
      pollingIntervalSeconds: 60,
      maxConcurrentTasks: 5,
      logFile: './AI_Employee_Vault/Logs/orchestrator.log',
      maxAttempts: 3,
      backoffFactor: 2,
      maxDelaySeconds: 60,
      dryRun: true,
      vaultPath: './AI_Employee_Vault',
      watchers: {
        gmail: {
          interval: 120,
          priorityKeywords: ['urgent', 'invoice', 'payment', 'asap', 'help']
        },
        whatsapp: {
          interval: 30,
          priorityKeywords: ['urgent', 'invoice', 'payment', 'asap', 'help']
        },
        filesystem: {
          interval: 60,
          watchFolders: ['./Downloads', './Inbox']
        }
      },
      approvalRules: {
        paymentsOver: 100,
        autoApproveThreshold: 50
      }
    };
    orchestrator = new Orchestrator(config);
  });

  test('should initialize with correct configuration', () => {
    expect(orchestrator).toBeDefined();
  });

  test('should have correct initial state', () => {
    expect(orchestrator['isRunning']).toBe(false);
    expect(orchestrator['taskQueue'].length).toBe(0);
    expect(orchestrator['activeTasks'].size).toBe(0);
  });
});