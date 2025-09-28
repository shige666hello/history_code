const GitHubDiscussionManager = require('./index.js');

async function demonstrateDiscussionNumber() {
  const token = process.env.GITHUB_TOKEN;
  const owner = 'shige666hello';
  const repo = 'history_code';

  if (!token) {
    console.error('请设置 GITHUB_TOKEN 环境变量');
    console.log('您可以通过以下方式获取 token:');
    console.log('1. 访问 https://github.com/settings/tokens');
    console.log('2. 创建新的 Personal Access Token');
    console.log('3. 设置环境变量: export GITHUB_TOKEN=your_token_here');
    process.exit(1);
  }

  const manager = new GitHubDiscussionManager(token, owner, repo);

  try {
    console.log('🚀 GitHub Discussions - DiscussionNumber 演示\n');

    // 1. 获取讨论分类
    console.log('📋 第一步: 获取讨论分类');
    const categories = await manager.getDiscussionCategories();
    
    if (categories.length === 0) {
      console.log('⚠️  该仓库没有启用 Discussions 或没有分类');
      console.log('请确保:');
      console.log('1. 仓库 Settings > Features > Discussions 已启用');
      console.log('2. 至少有一个讨论分类');
      return;
    }

    console.log('可用的讨论分类:');
    categories.forEach((category, index) => {
      console.log(`  ${index + 1}. ${category.name} (ID: ${category.id})`);
      if (category.description) {
        console.log(`     描述: ${category.description}`);
      }
    });

    // 2. 获取现有讨论
    console.log('\n📋 第二步: 获取现有讨论列表');
    const discussions = await manager.getDiscussions();

    if (discussions.length === 0) {
      console.log('当前没有讨论，让我们创建一个示例讨论');
      
      // 创建示例讨论
      console.log('\n📝 第三步: 创建示例讨论');
      const newDiscussion = await manager.createDiscussion(
        '示例讨论 - Node.js Workflow 演示',
        `这是一个通过 Node.js 脚本自动创建的讨论。

## 关于 DiscussionNumber
- DiscussionNumber 是讨论的唯一标识符
- 可以通过 API 获取: \`discussion.number\`
- 用于在代码中引用特定讨论
- 格式为整数，如: 1, 2, 3...

## 本演示展示了:
1. 如何获取 discussionNumber
2. 如何创建新讨论
3. 如何通过 number 获取讨论详情

创建时间: ${new Date().toISOString()}`,
        categories[0].id
      );

      console.log('✅ 新讨论已创建:');
      console.log(`   标题: ${newDiscussion.title}`);
      console.log(`   DiscussionNumber: ${newDiscussion.number}`);
      console.log(`   URL: ${newDiscussion.url}`);
      console.log(`   ID: ${newDiscussion.id}`);

      // 使用新创建的 discussion number
      console.log('\n🔍 第四步: 使用 DiscussionNumber 获取讨论详情');
      const discussionDetail = await manager.getDiscussionByNumber(newDiscussion.number);
      
      console.log(`讨论 #${newDiscussion.number} 的详细信息:`);
      console.log(`   标题: ${discussionDetail.title}`);
      console.log(`   作者: ${discussionDetail.author.login}`);
      console.log(`   分类: ${discussionDetail.category.name}`);
      console.log(`   创建时间: ${discussionDetail.createdAt}`);
      console.log(`   评论数: ${discussionDetail.comments.nodes.length}`);
      
    } else {
      console.log(`找到 ${discussions.length} 个现有讨论:`);
      discussions.forEach((discussion, index) => {
        console.log(`  ${index + 1}. #${discussion.number} - ${discussion.title}`);
        console.log(`     作者: ${discussion.author.login}`);
        console.log(`     分类: ${discussion.category.name}`);
        console.log(`     创建时间: ${discussion.createdAt}`);
        console.log('');
      });

      // 使用第一个讨论的 number 获取详情
      const firstDiscussion = discussions[0];
      console.log(`\n🔍 第三步: 使用 DiscussionNumber 获取讨论详情`);
      console.log(`获取讨论 #${firstDiscussion.number} 的详细信息...`);
      
      const discussionDetail = await manager.getDiscussionByNumber(firstDiscussion.number);
      
      console.log(`讨论 #${firstDiscussion.number} 的详细信息:`);
      console.log(`   标题: ${discussionDetail.title}`);
      console.log(`   作者: ${discussionDetail.author.login}`);
      console.log(`   分类: ${discussionDetail.category.name}`);
      console.log(`   创建时间: ${discussionDetail.createdAt}`);
      console.log(`   评论数: ${discussionDetail.comments.nodes.length}`);
      
      if (discussionDetail.comments.nodes.length > 0) {
        console.log('   最新评论:');
        discussionDetail.comments.nodes.slice(0, 3).forEach((comment, index) => {
          console.log(`     ${index + 1}. ${comment.author.login}: ${comment.body.substring(0, 50)}...`);
        });
      }
    }

    console.log('\n📚 DiscussionNumber 使用说明:');
    console.log('1. DiscussionNumber 是讨论的唯一数字标识符');
    console.log('2. 可以通过 API 获取: discussion.number');
    console.log('3. 用于在代码中引用特定讨论');
    console.log('4. 可以通过 number 获取讨论的完整信息');
    console.log('5. 在 GitHub URL 中使用: /discussions/{number}');

    console.log('\n🔧 API 端点示例:');
    console.log('获取讨论列表: GET /repos/{owner}/{repo}/discussions');
    console.log('获取特定讨论: GET /repos/{owner}/{repo}/discussions/{discussion_number}');
    console.log('创建讨论: POST /repos/{owner}/{repo}/discussions');

  } catch (error) {
    console.error('❌ 执行失败:', error.message);
    if (error.status === 404) {
      console.log('\n💡 提示:');
      console.log('1. 确保仓库已启用 Discussions 功能');
      console.log('2. 检查 token 是否有足够的权限');
      console.log('3. 确认仓库名称和所有者正确');
    }
    process.exit(1);
  }
}

// 如果直接运行此文件
if (require.main === module) {
  demonstrateDiscussionNumber();
}

module.exports = { demonstrateDiscussionNumber };
