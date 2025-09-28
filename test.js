const GitHubDiscussionManager = require('./index.js');

async function testDiscussionManager() {
  console.log('🧪 测试 GitHub Discussion Manager\n');

  const token = process.env.GITHUB_TOKEN;
  if (!token) {
    console.log('⚠️  未设置 GITHUB_TOKEN，运行模拟测试');
    console.log('设置环境变量 GITHUB_TOKEN 以运行实际测试');
    return;
  }

  const manager = new GitHubDiscussionManager(token, 'shige666hello', 'history_code');

  try {
    // 测试 1: 获取讨论分类
    console.log('测试 1: 获取讨论分类');
    const categories = await manager.getDiscussionCategories();
    console.log(`✅ 找到 ${categories.length} 个分类`);
    
    if (categories.length > 0) {
      console.log('前 3 个分类:');
      categories.slice(0, 3).forEach(cat => {
        console.log(`  - ${cat.name}: ${cat.description || '无描述'}`);
      });
    }

    // 测试 2: 获取讨论列表
    console.log('\n测试 2: 获取讨论列表');
    const discussions = await manager.getDiscussions();
    console.log(`✅ 找到 ${discussions.length} 个讨论`);

    if (discussions.length > 0) {
      console.log('前 3 个讨论:');
      discussions.slice(0, 3).forEach(discussion => {
        console.log(`  - #${discussion.number}: ${discussion.title}`);
        console.log(`    作者: ${discussion.author.login}`);
        console.log(`    分类: ${discussion.category.name}`);
      });

      // 测试 3: 获取特定讨论
      console.log('\n测试 3: 获取特定讨论详情');
      const testDiscussion = discussions[0];
      const detail = await manager.getDiscussionByNumber(testDiscussion.number);
      
      console.log(`讨论 #${testDiscussion.number} 详情:`);
      console.log(`  标题: ${detail.title}`);
      console.log(`  作者: ${detail.author.login}`);
      console.log(`  创建时间: ${detail.createdAt}`);
      console.log(`  评论数: ${detail.comments.nodes.length}`);
      console.log(`  内容长度: ${detail.body.length} 字符`);
    }

    console.log('\n✅ 所有测试通过!');

  } catch (error) {
    console.error('❌ 测试失败:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  testDiscussionManager();
}

module.exports = { testDiscussionManager };
// test change
