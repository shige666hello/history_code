const { Octokit } = require('@octokit/rest');

class GitHubDiscussionManager {
  constructor(token, owner, repo) {
    this.octokit = new Octokit({ auth: token });
    this.owner = owner;
    this.repo = repo;
  }

  async getDiscussions(categoryId = null) {
    try {
      const query = `
        query($owner: String!, $repo: String!, $categoryId: ID) {
          repository(owner: $owner, name: $repo) {
            discussions(first: 10, categoryId: $categoryId) {
              nodes {
                id
                number
                title
                body
                createdAt
                author {
                  login
                }
                category {
                  name
                }
              }
            }
          }
        }
      `;

      const response = await this.octokit.graphql(query, {
        owner: this.owner,
        repo: this.repo,
        categoryId: categoryId
      });

      return response.repository.discussions.nodes;
    } catch (error) {
      console.error('Error fetching discussions:', error);
      throw error;
    }
  }

  async createDiscussion(title, body, categoryId) {
    try {
      const query = `
        mutation($repositoryId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
          createDiscussion(input: {
            repositoryId: $repositoryId,
            categoryId: $categoryId,
            title: $title,
            body: $body
          }) {
            discussion {
              id
              number
              title
              url
            }
          }
        }
      `;

      // 首先获取仓库 ID
      const repoQuery = `
        query($owner: String!, $repo: String!) {
          repository(owner: $owner, name: $repo) {
            id
          }
        }
      `;

      const repoResponse = await this.octokit.graphql(repoQuery, {
        owner: this.owner,
        repo: this.repo
      });

      const repositoryId = repoResponse.repository.id;

      const response = await this.octokit.graphql(query, {
        repositoryId: repositoryId,
        categoryId: categoryId,
        title: title,
        body: body
      });

      return response.createDiscussion.discussion;
    } catch (error) {
      console.error('Error creating discussion:', error);
      throw error;
    }
  }

  async getDiscussionCategories() {
    try {
      const query = `
        query($owner: String!, $repo: String!) {
          repository(owner: $owner, name: $repo) {
            discussionCategories(first: 10) {
              nodes {
                id
                name
                description
              }
            }
          }
        }
      `;

      const response = await this.octokit.graphql(query, {
        owner: this.owner,
        repo: this.repo
      });

      return response.repository.discussionCategories.nodes;
    } catch (error) {
      console.error('Error fetching discussion categories:', error);
      throw error;
    }
  }

  async getDiscussionByNumber(number) {
    try {
      const query = `
        query($owner: String!, $repo: String!, $number: Int!) {
          repository(owner: $owner, name: $repo) {
            discussion(number: $number) {
              id
              number
              title
              body
              createdAt
              author {
                login
              }
              category {
                name
              }
              comments(first: 10) {
                nodes {
                  id
                  body
                  author {
                    login
                  }
                  createdAt
                }
              }
            }
          }
        }
      `;

      const response = await this.octokit.graphql(query, {
        owner: this.owner,
        repo: this.repo,
        number: number
      });

      return response.repository.discussion;
    } catch (error) {
      console.error('Error fetching discussion by number:', error);
      throw error;
    }
  }
}

// 示例使用
async function main() {
  const token = process.env.GITHUB_TOKEN;
  const owner = 'shige666hello';
  const repo = 'history_code';

  if (!token) {
    console.error('请设置 GITHUB_TOKEN 环境变量');
    process.exit(1);
  }

  const manager = new GitHubDiscussionManager(token, owner, repo);

  try {
    console.log('=== 获取讨论分类 ===');
    const categories = await manager.getDiscussionCategories();
    console.log('讨论分类:', categories);

    console.log('\n=== 获取最近的讨论 ===');
    const discussions = await manager.getDiscussions();
    console.log('讨论列表:', discussions);

    if (discussions.length > 0) {
      console.log('\n=== 获取特定编号的讨论 ===');
      const discussionNumber = discussions[0].number;
      const discussion = await manager.getDiscussionByNumber(discussionNumber);
      console.log(`讨论 #${discussionNumber}:`, discussion);
    }

    console.log('\n=== 创建新讨论示例 ===');
    console.log('要创建讨论，请使用以下代码:');
    console.log(`
    const newDiscussion = await manager.createDiscussion(
      '新的讨论标题',
      '这是讨论的内容',
      categories[0].id
    );
    console.log('新讨论:', newDiscussion);
    `);

  } catch (error) {
    console.error('执行失败:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = GitHubDiscussionManager;
